import torch
from gfpgan import GFPGANer
from diffusers import (
    AutoencoderKL, 
    StableDiffusionControlNetImg2ImgPipeline, 
    DPMSolverMultistepScheduler, 
    ControlNetModel
)
from transformers import logging as transformers_logging
import os

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