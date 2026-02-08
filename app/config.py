import os
from pathlib import Path
from dotenv import load_dotenv


ROOT_DIR = Path(__file__).resolve().parents[1]
load_dotenv(ROOT_DIR / ".env")

CLOUDINARY_NAME = os.getenv("CLOUDINARY_NAME")
CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
CLOUDINARY_SECRET_KEY = os.getenv("CLOUDINARY_SECRET_KEY")

MODEL_PATH = os.getenv("MODEL_PATH")
OUTPUT_DIR = os.getenv("OUTPUT_DIR") or str(ROOT_DIR / "outputs")
LORA_DIR = os.getenv("LORA_DIR")
CONTROLNET_PATH = os.getenv("CONTROLNET_PATH")
GFPGAN_PATH = os.getenv("GFPGAN_PATH")
