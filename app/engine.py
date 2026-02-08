import torch
import os
import time
from config import MODEL_PATH, OUTPUT_DIR, LORA_DIR, CONTROLNET_PATH, GFPGAN_PATH
from model_loader import (
    load_vae, 
    load_controlnet, 
    load_pipeline, 
    load_lora, 
    load_gfpgan
)
from utils import (
    scale_down_image, 
    get_canny_image, 
    restore_face, 
    generate_random_seed
)

os.makedirs(OUTPUT_DIR, exist_ok=True)

class NeuroMorph:
    def __init__(self):
        self.pipe = None
        self.face_restorer = None
    
    def setup(self):
        """Initialize all models and pipeline"""
        start_setup = time.time()
        print("Memulai setup model dan pipeline...")
        
        # Load all models
        vae = load_vae()
        controlnet = load_controlnet(CONTROLNET_PATH)
        self.pipe = load_pipeline(MODEL_PATH, controlnet, vae)
        self.pipe = load_lora(self.pipe, LORA_DIR)
        self.face_restorer = load_gfpgan(GFPGAN_PATH)
        
        duration = time.time() - start_setup
        print(f"Setup selesai dalam {duration:.2f} detik. Sistem siap!")
    
    def generate(self, image_path, prompt, negative_prompt, steps, strength, lora_scale=0.6, guidance_scale=7.5):
        """Generate transformed image with AI"""
        print("Memulai proses generate gambar...")
        start_gen = time.time()
        
        # Prepare images
        r_image = scale_down_image(image_path, 768)
        canny_image = get_canny_image(r_image, low=30, high=80)
        canny_image.save(os.path.join(OUTPUT_DIR, "debug_canny.png"))
        
        # Generate seed
        seed = generate_random_seed()
        generator = torch.Generator('cuda').manual_seed(seed)
        
        # AI Diffusion
        start_diffusion = time.time()
        output = self.pipe(
            prompt=prompt,
            image=r_image,
            control_image=canny_image,
            strength=strength,
            negative_prompt=negative_prompt,
            num_inference_steps=steps,
            generator=generator,
            guidance_scale=guidance_scale,
            controlnet_conditioning_scale=0.95,
            cross_attention_kwargs={"scale": lora_scale}
        ).images[0]
        diffusion_time = time.time() - start_diffusion
        
        # Face Restoration
        start_restore = time.time()
        clean_output = restore_face(self.face_restorer, output)
        restore_time = time.time() - start_restore
        
        total_duration = time.time() - start_gen
        
        # Print statistics
        self._print_stats(diffusion_time, restore_time, total_duration)
        
        return clean_output
    
    def _print_stats(self, diffusion_time, restore_time, total_duration):
        """Print generation statistics"""
        print(f"--- Statistik Kecepatan ---")
        print(f"Difusi AI       : {diffusion_time:.2f} detik")
        print(f"Restorasi Wajah : {restore_time:.2f} detik")
        print(f"Total Proses    : {total_duration:.2f} detik")
        print(f"---------------------------")
