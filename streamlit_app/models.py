import torch
import streamlit as st

from fish_speech.inference_engine import TTSInferenceEngine
from fish_speech.models.dac.inference import load_model as load_decoder_model
from fish_speech.models.text2semantic.inference import launch_thread_safe_queue

from config import get_config

@st.cache_resource
def load_tts_engine() -> TTSInferenceEngine:

    # carico il motore TTS completo
    config = get_config()

    st.info(f"Caricamento modelli su {config.device}...")

    # carico il modello Llama
    llama_queue = launch_thread_safe_queue(
        checkpoint_path=config.llama_checkpoint_path,
        device=config.device,
        precision=config.precision,
        compile=config.compile
    )

    # carico il modello decoder
    decoder_model = load_decoder_model(
        checkpoint_path=config.decoder_checkpoint_path,
        config_name=config.decoder_config_name,
        device=config.device,
    )

    # creo il motore di inferenza TTS
    inference_engine = TTSInferenceEngine(
        llama_queue=llama_queue,
        decoder_model=decoder_model,
        compile=config.compile,
        precision=config.precision,
    )

    return inference_engine

def get_device_info() -> dict:
    config = get_config()

    return {
        "device" : config.device,
        "device_name" : torch.cuda.get_device_name(0) if torch.cuda.is_available() else "CPU",
        "cuda_avaiable" : torch.cuda.is_available(),
        "memory_allocated" : torch.cuda.memory_allocated(0) if torch.cuda.is_available() else 0,
    }