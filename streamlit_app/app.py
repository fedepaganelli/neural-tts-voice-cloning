import streamlit as st
import torch
from utils import setup_page, get_custom_css, create_parameter_sidebar, display_audio_player, display_reference_audio_preview
from inference import synthesize_text, prepare_reference_audio, audio_to_buffer
from models import get_device_info

setup_page()
st.markdown(get_custom_css(), unsafe_allow_html=True)

st.markdown('<div class="main-header"> Applicazione TTS con Fish-Speech </div>', unsafe_allow_html=True)
st.markdown("Texto-to-Speech (TTS) Inference WebUI")

col1, col2 = st.columns([3,2])

with col1:

    st.markdown("### Testo di Input")
    text_input = st.text_area("Input Text", height=150, key="text_input", placeholder="Inserisci il testo da sintetizzare qui...")

    st.markdown("### Audio di Riferimento (opzionale)")
    reference_audio = st.file_uploader("Carica l'audio di riferimento", type=["wav", "mp3"], key="reference_audio")
    reference_id = st.text_input("Reference ID", placeholder="voce di riferimento", key="reference_id")

    reference_buffer = None
    if reference_audio is not None:
        reference_buffer = display_reference_audio_preview(reference_audio)

with col2:

    params = create_parameter_sidebar()
    if st.button("Genera Audio", type="primary", use_container_width=True):
        if text_input.strip():
            with st.spinner(" Generazione audio in corso..."):

                references = []
                if reference_audio:
                    ref_audio = prepare_reference_audio(reference_audio)
                    if ref_audio:
                        references = [ref_audio]

                audio_data, sample_rate = synthesize_text(
                    text_input,
                    references=references,
                    reference_id=reference_id if reference_id else None,
                    **params
                )

                if audio_data is not None:

                    audio_buffer = audio_to_buffer(audio_data, sample_rate)
                    if audio_buffer:
                        display_audio_player(audio_buffer)
                        st.success("Audio generato con successo!")
                    else:
                        st.error("Errore nella conversione dell'audio in buffer.")
                else:
                    st.error("Nessun audio generato, controlla il testo di input.")
        else:
            st.warning("Per favore, inserisci del testo da sintetizzare.")

st.markdown("---")
st.caption("Applicazione TTS con Fish-Speech - Streamlit WebUI")
with st.expander("Come funziona l'app"):
    st.markdown("""
    1. **Inserisci il testo** da sintetizzare
    2. **Carica un audio** di riferimento (opzionale, per voice cloning)
    3. **Regola i parametri** nella sidebar se necessario
    4. **Clicca Generate Audio** per creare l'audio
    5. **Ascolta e confronta** l'audio generato con il reference
    6. **Scarica** gli audio che preferisci
    """)