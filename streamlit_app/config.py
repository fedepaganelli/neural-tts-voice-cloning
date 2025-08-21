from pathlib import Path
from dataclasses import dataclass
import torch

@dataclass
class AppConfig:

    # percorso dei modelli
    llama_checkpoint_path: Path = Path(__file__).parent.parent / "fish-speech" / "checkpoints" / "openaudio-s1-mini"
    decoder_checkpoint_path: Path = Path(__file__).parent.parent / "fish-speech" / "checkpoints" / "openaudio-s1-mini" / "codec.pth"
    decoder_config_name: str = "modded_dac_vq"

    # impostazioni del dispositivo
    device: str = "cuda" if torch.cuda.is_available() else "cpu"
    precision : torch.dtype = torch.bfloat16
    compile: bool = False

    # impostazioni dell'interfaccia
    default_max_tokens: int = 1024
    default_chunk_length : int = 200
    default_temperature: float = 0.7
    default_top_p: float = 0.7
    default_repetition_penalty: float = 1.5

    # impostazione per l'audio
    sample_rate: int = 44100

def get_config() -> AppConfig:
    return AppConfig()
