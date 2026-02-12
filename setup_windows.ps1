Write-Host "=== CREATE VENV ==="
python -m venv venv
.\venv\Scripts\activate

Write-Host "=== UPGRADE PIP ==="
pip install --upgrade pip setuptools wheel

Write-Host "=== INSTALL PYTORCH CUDA ==="
pip install torch torchvision torchaudio `
  --index-url https://download.pytorch.org/whl/cu121

Write-Host "=== INSTALL REQUIREMENTS ==="
pip install -r requirements.txt

Write-Host "=== SET ENV VARS ==="
[Environment]::SetEnvironmentVariable(
  "MODEL_PATH",
  "D:\models\base_model\Realistic_Vision_V6.0_NV_B1_fp16.safetensors",
  "User"
)
[Environment]::SetEnvironmentVariable("OUTPUT_DIR", "D:\output", "User")
[Environment]::SetEnvironmentVariable(
  "LORA_ANIME",
  "D:\models\lora\anime.safetensors",
  "User"
)
[Environment]::SetEnvironmentVariable(
  "LORA_GHIBLI",
  "D:\models\lora\ghibli.safetensors",
  "User"
)
[Environment]::SetEnvironmentVariable(
  "LORA_ZOOTOPIA",
  "D:\models\lora\zootopia.safetensors",
  "User"
)
[Environment]::SetEnvironmentVariable(
  "CONTROLNET_PATH",
  "D:\models\controlnet\canny",
  "User"
)
[Environment]::SetEnvironmentVariable(
  "GFPGAN_PATH",
  "D:\models\restoration\GFPGANv1.3.pth",
  "User"
)

Write-Host "=== WINDOWS SETUP COMPLETE ==="
