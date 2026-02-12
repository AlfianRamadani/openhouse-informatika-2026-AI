import os
from pathlib import Path
from dotenv import load_dotenv


ROOT_DIR = Path(__file__).resolve().parents[1]
load_dotenv(ROOT_DIR / ".env")

CLOUDINARY_NAME = os.getenv("CLOUDINARY_NAME")
CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
CLOUDINARY_SECRET_KEY = os.getenv("CLOUDINARY_SECRET_KEY")

def _get_env_path(name):
    value = os.getenv(name)
    return value if value and value.strip() else None

MODEL_PATH = _get_env_path("MODEL_PATH")
OUTPUT_DIR = _get_env_path("OUTPUT_DIR") or str(ROOT_DIR / "outputs")

# LoRA configuration
# Backward compatible: if LORA_ANIME is not set, fallback to LORA_DIR.
LORA_DIR = _get_env_path("LORA_DIR")
LORA_ANIME = _get_env_path("LORA_ANIME")
LORA_PATHS = {
    "anime": LORA_ANIME
}
LORA_PATHS = {k: v for k, v in LORA_PATHS.items() if v}

CONTROLNET_PATH = _get_env_path("CONTROLNET_PATH")
GFPGAN_PATH = _get_env_path("GFPGAN_PATH")
