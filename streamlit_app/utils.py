import streamlit as st
from typing import Any, Dict, Optional
import torch
from io import BytesIO

def setup_page() -> None:

    # configuro la pagina di Streamlit
    st.set_page_config(
        page_title="Applicazione TTS con Fish-Speech",
        page_icon="🗣️",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def get_custom_css() -> str:

    # per testo personalizzato con CSS
    return """
    <style>
        .main-header { font-size: 2.5rem !important; font-weight: bold !important; color: #1f77b4 !important; }
        .section-header { font-size: 1.5rem !important; font-weight: bold !important; color: #333 !important; }
        .param-container { background-color: #f8f9fa; padding: 1rem; border-radius: 8px; margin-bottom: 1rem; }
    </style>
    """

def create_parameter_sidebar() -> Dict[str, Any]:

    # creo la sidebar per i parametri
    with st.sidebar:
        st.markdown("### Paramtri di Sintesi")

        params = {
            "max_new_tokens": st.slider("Max Tokens", 256, 4096, 1024),
            "chunk_length": st.slider("Chunk Length (ms)", 100, 500, 200),
            "temperature": st.slider("Temperature", 0.0, 1.0, 0.7,0.1),
            "top_p": st.slider("Top-p", 0.1, 1.0, 0.7,0.1),
            "repetition_penalty": st.slider("Repetition Penalty", 1.0, 2.0, 1.5,0.1),

        }

        # info sul sistema in uso
        st.markdown("---")
        st.markdown("### Info Sistema")
        if torch.cuda.is_available():
            st.success("GPU disponibile")
        else:
            st.warning("CPU in uso, le prestazioni potrebbero essere limitate.")

        return params

def display_audio_player(audio_buffer, key_suffix: str = "") -> None:

    # visualizzo il player audio
    if audio_buffer:
        st.audio(audio_buffer, format="audio/wav")

        st.download_button(
            label="Download Audio",
            data=audio_buffer,
            file_name="audio_output.wav",
            mime="audio/wav",
            use_container_width=True,
            key=f"download_{key_suffix}"
        )



def display_reference_audio_preview(uploaded_file) -> Optional[BytesIO]:
    if uploaded_file is None:
        return None

    try:

        from inference import process_uploaded_audio

        audio_buffer, sample_rate = process_uploaded_audio(uploaded_file)

        if audio_buffer:

            st.markdown('<div class="audio-preview">', unsafe_allow_html=True)
            st.success("Audio di riferimento caricato correttamente!")
            display_audio_player(audio_buffer, "Anteprima Audio di Riferimento")
            st.markdown('</div>', unsafe_allow_html=True)
            return audio_buffer
        else:
            st.warning("Impossibile processare l'audio di riferimento")

    except Exception as e:
        st.error(f"Errore nel processing dell'audio: {str(e)}")

    return None