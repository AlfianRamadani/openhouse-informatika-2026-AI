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

def load_lora(pipe, lora_path, adapter_name="lora"):
    """Load LoRA weights (single adapter)"""
    print(f"Loading LoRA weights: {adapter_name}")
    if not os.path.exists(lora_path):
        raise FileNotFoundError(f"File LoRA tidak ditemukan di: {lora_path}")
    
    try:
        pipe.load_lora_weights(lora_path, adapter_name=adapter_name)
    except Exception as e:
        print(f"Mencoba metode alternatif untuk loading LoRA: {e}")
        lora_folder = os.path.dirname(lora_path)
        lora_filename = os.path.basename(lora_path)
        pipe.load_lora_weights(
            lora_folder, 
            weight_name=lora_filename, 
            adapter_name=adapter_name
        )
    
    return pipe

def load_loras(pipe, lora_paths, fallback_path=None):
    """Load multiple LoRA adapters if provided, otherwise fallback to single LoRA."""
    loaded_adapters = []
    if lora_paths:
        for name, path in lora_paths.items():
            if not path:
                continue
            pipe = load_lora(pipe, path, adapter_name=name)
            loaded_adapters.append(name)
    elif fallback_path:
        pipe = load_lora(pipe, fallback_path, adapter_name="lora")
        loaded_adapters.append("lora")
    
    return pipe, loaded_adapters

def load_gfpgan(gfpgan_path):
    """Load GFPGAN face restorer"""
    print("Loading GFPGAN...")
    return GFPGANer(
        model_path=gfpgan_path, 
        upscale=1, 
        arch='clean', 
        channel_multiplier=2
    )
