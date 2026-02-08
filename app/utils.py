import os
import random
import cv2
import numpy as np
from PIL import Image
import torch
from gfpgan import GFPGANer
from diffusers import (
    AutoencoderKL,
    StableDiffusionControlNetImg2ImgPipeline,
    DPMSolverMultistepScheduler,
    ControlNetModel,
)
from transformers import logging as transformers_logging

transformers_logging.set_verbosity_error()

def load_vae():
    """Load VAE model"""
    print("Loading VAE...")
    return AutoencoderKL.from_pretrained(
        "stabilityai/sd-vae-ft-mse", 
        torch_dtype=torch.float16
    ).to("cuda")

def load_controlnet(controlnet_path):
    """Load ControlNet model"""
    print("Loading ControlNet...")
    return ControlNetModel.from_pretrained(
        controlnet_path, 
        torch_dtype=torch.float16
    ).to("cuda")

def load_pipeline(model_path, controlnet, vae):
    """Load Stable Diffusion pipeline"""
    print("Loading Stable Diffusion pipeline...")
    pipe = StableDiffusionControlNetImg2ImgPipeline.from_single_file(
        model_path,
        controlnet=controlnet,
        vae=vae,
        torch_dtype=torch.float16,
        load_safety_checker=False,
        use_safetensors=True
    ).to("cuda")
    
    # Disable safety checker
    pipe.safety_checker = None
    pipe.feature_extractor = None
    
    # Set scheduler
    pipe.scheduler = DPMSolverMultistepScheduler.from_config(
        pipe.scheduler.config
    )
    
    return pipe

def load_lora(pipe, lora_dir):
    """Load LoRA weights"""
    print("Loading LoRA weights...")
    if not os.path.exists(lora_dir):
        raise FileNotFoundError(f"File LoRA tidak ditemukan di: {lora_dir}")
    
    try:
        pipe.load_lora_weights(lora_dir, adapter_name="lora")
    except Exception as e:
        print(f"Mencoba metode alternatif untuk loading LoRA: {e}")
        lora_folder = os.path.dirname(lora_dir)
        lora_filename = os.path.basename(lora_dir)
        pipe.load_lora_weights(
            lora_folder, 
            weight_name=lora_filename, 
            adapter_name="lora"
        )
    
    return pipe

def load_gfpgan(gfpgan_path):
    """Load GFPGAN face restorer"""
    print("Loading GFPGAN...")
    return GFPGANer(
        model_path=gfpgan_path, 
        upscale=1, 
        arch='clean', 
        channel_multiplier=2
    )

def scale_down_image(image_path, target_size=768):
    """Load image and scale down while preserving aspect ratio."""
    image = Image.open(image_path).convert("RGB")
    width, height = image.size
    max_dim = max(width, height)
    if max_dim <= target_size:
        return image
    scale = target_size / max_dim
    new_size = (int(width * scale), int(height * scale))
    return image.resize(new_size, Image.LANCZOS)

def get_canny_image(image_pil, low=30, high=80):
    """Generate Canny edge map from PIL image and return PIL image."""
    image_np = np.array(image_pil)
    gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)
    edges = cv2.Canny(gray, low, high)
    edges_3ch = np.stack([edges] * 3, axis=-1)
    return Image.fromarray(edges_3ch)

def restore_face(face_restorer, image_pil):
    """Restore face details using GFPGAN and return PIL image."""
    image_np = np.array(image_pil)
    image_bgr = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
    try:
        _, _, restored_bgr = face_restorer.enhance(
            image_bgr,
            has_aligned=False,
            only_center_face=False,
            paste_back=True
        )
    except Exception:
        restored_bgr = image_bgr
    restored_rgb = cv2.cvtColor(restored_bgr, cv2.COLOR_BGR2RGB)
    return Image.fromarray(restored_rgb)

def generate_random_seed():
    """Generate a random seed for reproducible diffusion results."""
    return random.randint(0, 2**32 - 1)
