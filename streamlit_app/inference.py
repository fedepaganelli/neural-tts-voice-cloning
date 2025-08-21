import numpy as np
import io
import soundfile as sf
from typing import Tuple, Optional
import streamlit as st
import librosa
from fish_speech.utils.schema import ServeTTSRequest, ServeReferenceAudio
from models import load_tts_engine

def synthesize_text(text: str, **kwargs) -> Tuple[Optional[np.ndarray], Optional[int]]:

    # sintetizzo il testo in audio
    try:
        inference_engine = load_tts_engine()

        request = ServeTTSRequest(
            text=text,
            references=kwargs.get('references',[]),
            reference_id=kwargs.get('reference_id'),
            max_new_tokens=kwargs.get('max_new_tokens', 1024),
            chunk_length=kwargs.get('chunk_length', 200),
            top_p=kwargs.get('top_p', 0.7),
            repetition_penalty=kwargs.get('repetition_penalty', 1.5),
            temperature=kwargs.get('temperature', 0.7),
            format="wav",
            streaming=False,
        )

        # eseguo l'inferenza

        for result in inference_engine.inference(request):
            if result.code == "error" :
                raise RuntimeError(f"Errore durante l'inferenza: {result.error}")

            elif result.code == "final":
                sample_rate, audio_data = result.audio
                return audio_data, sample_rate

        raise RuntimeError("Nessun audio generato, controlla il testo di input.")

    except Exception as e:
        st.error(f" Errore durante la sintesi del testo: {str(e)}")
        return None, None

def prepare_reference_audio(uploaded_file) -> Optional[ServeReferenceAudio]:

    # preparo l'audio di riferimento
    if uploaded_file is None:
        return None

    try:
        audio_bytes = uploaded_file.getvalue()
        return ServeReferenceAudio(audio=audio_bytes, text="reference")
    except Exception as e:
        st.warning(f" Impossibile processare il file audio di riferimento: {e}")
        return None

def audio_to_buffer(audio_data: np.ndarray, sample_rate: int) -> io.BytesIO:

    # converto l'audio in un buffer
    if audio_data is None or len(audio_data) == 0:
        return None

    # normalizzo l'audio
    max_val = np.max(np.abs(audio_data))
    if max_val > 0:
        audio_data = audio_data / max_val

    # salvo l'audio in un buffer
    buffer = io.BytesIO()
    sf.write(buffer, audio_data, sample_rate, format='WAV')
    buffer.seek(0)

    return buffer


def process_uploaded_audio(uploaded_file):
    if uploaded_file is None:
        return None, None

    try:
        audio_bytes = uploaded_file.getvalue()

        temp_buffer = io.BytesIO(audio_bytes)

        audio_data, sr = librosa.load(temp_buffer, sr=None)

        max_val = np.max(np.abs(audio_data))
        if max_val > 0:
            audio_data = audio_data / max_val

        buffer = io.BytesIO()
        sf.write(buffer, audio_data, sr, format='WAV')
        buffer.seek(0)

        return buffer, sr

    except Exception as e:
        st.warning(f"Impossibile processare l'audio: {e}")
        return None, None