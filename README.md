# 🗣️ Applicazione TTS con Fish-Speech

Interfaccia Streamlit per sintesi vocale avanzata utilizzando il framework Fish-Speech e il modello OpenAudio S1 Mini. 
Interfaccia utente per generare audio di alta qualità con supporto per voice cloning e gestione avanzata dei parametri.

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)

## Caratteristiche

- **Sintesi vocale di alta qualità** con OpenAudio S1 Mini
- **Interfaccia Streamlit** intuitiva e user-friendly
- **Voice cloning** con audio di riferimento
- **Controllo avanzato** dei parametri di generazione
- **Download** degli audio generati
- **Supporto per più formati** (WAV, MP3, OGG, FLAC)

## Prerequisiti

- Python 3.12
- GPU  (consigliata) o CPU ma con prestazioni limitate
- 8GB+ RAM
- 4GB+ spazio libero per i modelli

## Installazione

### 1. Clona il repository

```bash
git clone https://github.com/tuo-username/fish-speech-tts-app.git
cd fish-speech-tts-app

```

### 2. Clona il repository di Fish-Speech

```bash
git clone https://github.com/fishaudio/fish-speech.git
cd fish-speech

```

### 3. Setup dell'ambiente virtuale

- per prima cosa bisogna installare pyaudio e sox, i quali sono necessari per la sintesi vocale e la gestione degli audio.

```bash
apt install portaudio19-dev libsox-dev ffmpeg

```

- installazione dell'ambiente virtuale

```bash

conda create -n fish-speech python=3.12
conda activate fish-speech

pip install -e .
```
- in merito agli ultimi step si consiglia di visionare la documentazione ufficiale di Fish-Speech per eventuali aggiornamenti o modifiche.
https://github.com/fishaudio/fish-speech/blob/main/docs/en/install.md

### 4. Download dei modelli
- per prima cosa bisogna scaricare i modelli necessari per la sintesi vocale, in questo caso il modello OpenAudio S1 Mini.

```bash
huggingface-cli download fishaudio/openaudio-s1-mini --local-dir checkpoints/openaudio-s1-mini
```
nota bene: è necessario avere un account Hugging Face e configurare il token di accesso per scaricare i modelli.
Per creare un token è possibile accede alla pagina delle impostazioni su Hugging Face.

_Inoltre è necessario accettare i termini di utilizzo del modello OpenAudio S1 Mini prima di poterlo scaricare._

https://github.com/fishaudio/fish-speech/blob/main/docs/en/inference.md

### 5. Installazione delle dipendenze dell'applicazione

```bash
cd streamlit_app
pip install -r requirements.txt
```

### 6. Avvio dell'applicazione

```bash
streamlit run app.py
```

L'applicazione sarà disponibile all'indirizzo `http://localhost:8501`.

###  Utilizzo

- **Input di testo**: Inserisci il testo da convertire in audio.
- **Audio di riferimento**: Carica un file audio per il voice cloning (opzionale).
- **Parametri di generazione**: Regola i parametri nella sidebar per personalizzare la sintesi vocale.
- **Genera audio**: Clicca su "Genera Audio" per avviare la sintesi vocale.
- **Ascolta l'audio**: Dopo la generazione, puoi ascoltare l'audio direttamente nell'app.
- **Download**: Scarica l'audio generato

#### Parametri configurabili:
- **Temperature** (0.1-1.0): Controlla la casualità della generazione
- **Top-p** (0.1-1.0): Filtra i token meno probabili
- **Repetition Penalty** (1.0-2.0): Riduce le ripetizioni
- **Max Tokens** (256-4096): Limita la lunghezza massima
- **Chunk Length** (100-500ms): Dimensione dei chunk di processing