# Openhouse Informatika 2026 AI Style Transfer

**General**
This project is a simple photo booth that turns a visitor photo into a stylized image. The visitor stands in front of a webcam, takes a photo, chooses a style, and the system generates a new image. The result is shown on the laptop screen and can be downloaded using a QR code on a phone.

**Flow**
This section follows the flow in the diagram.
1. Visitor stands in front of the webcam and clicks "Take Photo".
2. Visitor selects a style prompt (anime, ghibli, or zootopia).
3. The laptop sends the photo and prompt to the local GPU for rendering.
4. The GPU returns a rendered image (PNG or JPEG) to the laptop.
5. The laptop uploads the image to the internet (Cloudinary).
6. Cloudinary returns a public URL for download.
7. The laptop generates a QR code from the public URL.
8. Visitor scans the QR code with a phone using a private internet connection.
9. The phone downloads the image directly.

**Architecture**
- UI layer: `app/app.py` (Streamlit). Handles camera input, style selection, progress UI, and result display.
- Inference engine: `app/engine.py` (`NeuroMorph`). Orchestrates preprocessing, diffusion, and face restoration.
- Model loading: `app/model_loader.py`. Loads VAE, ControlNet, Stable Diffusion pipeline, LoRA, and GFPGAN.
- Prompts and settings: `app/prompts.py`. Defines positive and negative prompts per style.
- Cloud upload and QR: `app/cloud_manager.py`. Uploads to Cloudinary and generates QR code.
- Configuration: `app/config.py`. Reads environment variables from `.env`.
- Assets: `models/` for model files and `outputs/` or `OUTPUT_DIR` for generated images.

**Mechanism**
This section describes the technical steps in code.
1. Streamlit captures a photo with `st.camera_input` and stores it in session state.
2. The app saves the photo to `OUTPUT_DIR` and loads the cached `NeuroMorph` pipeline.
3. The engine expects to preprocess the image by resizing to 768 px, generating a Canny edge map, and creating a random seed.
4. The diffusion pipeline is executed with ControlNet guidance, FP16, and a LoRA adapter, using the selected `guidance_scale` from the UI.
5. GFPGAN restores facial details on the generated image.
6. The result is saved locally and optionally uploaded to Cloudinary for a public URL.
7. A QR code is generated and displayed so the visitor can download the image on a phone.

**Model**
- Base model: Stable Diffusion 1.5 image-to-image pipeline loaded from a local `.safetensors` file.
- VAE: `stabilityai/sd-vae-ft-mse`.
- ControlNet: Canny edge guidance loaded from local `CONTROLNET_PATH`.
- LoRA: Style adapters loaded from `LORA_ANIME`, `LORA_GHIBLI`, `LORA_ZOOTOPIA` (falls back to `LORA_DIR`).
- Scheduler: `DPMSolverMultistepScheduler`.
- Face restoration: `GFPGAN` (used after diffusion).
- Execution: CUDA, FP16, local GPU required.

**Other Explanation**
Setup and run:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python scripts/health_check.py
streamlit run app/app.py
```

Environment configuration:
The app reads configuration from `.env` or exported environment variables.
```bash
MODEL_PATH=/absolute/path/to/base_model.safetensors
OUTPUT_DIR=/absolute/path/to/outputs
LORA_ANIME=/absolute/path/to/anime.safetensors
LORA_GHIBLI=/absolute/path/to/ghibli.safetensors
LORA_ZOOTOPIA=/absolute/path/to/zootopia.safetensors
LORA_DIR=/absolute/path/to/lora.safetensors  # optional fallback if you only have one LoRA
CONTROLNET_PATH=/absolute/path/to/controlnet/canny
GFPGAN_PATH=/absolute/path/to/GFPGANv1.3.pth

CLOUDINARY_NAME=your_cloudinary_name
CLOUDINARY_API_KEY=your_cloudinary_key
CLOUDINARY_SECRET_KEY=your_cloudinary_secret
```

Dependencies:
Python packages are listed in `requirements.txt`.

Defaults:
- If `OUTPUT_DIR` is not set, outputs are saved to `./outputs`.

Cloudinary compatibility:
- The uploader accepts both `CLOUDINARY_*` and the legacy `CLOUD_NAME`, `API_KEY`, `API_SECRET` variables.

Health check:
- Run `python scripts/health_check.py` to verify GPU availability and model paths.

Project structure:
- `app/app.py` Streamlit UI and user flow
- `app/engine.py` Inference orchestration
- `app/model_loader.py` Model loading helpers
- `app/cloud_manager.py` Cloudinary upload and QR
- `app/prompts.py` Prompts and default settings
- `models/` Local model files
- `outputs/` Generated images (or set via `OUTPUT_DIR`)
