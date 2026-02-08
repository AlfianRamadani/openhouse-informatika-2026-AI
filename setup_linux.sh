#!/bin/bash
set -e

echo "=== SYSTEM UPDATE ==="
sudo apt update && sudo apt upgrade -y

echo "=== INSTALL SYSTEM DEPENDENCIES ==="
sudo apt install -y \
  git wget python3 python3-venv python3-pip \
  ffmpeg libgl1 libglib2.0-0

echo "=== CREATE VENV ==="
python3 -m venv venv
source venv/bin/activate

echo "=== UPGRADE PIP ==="
pip install --upgrade pip setuptools wheel

echo "=== INSTALL PYTORCH CUDA ==="
pip install torch torchvision torchaudio \
  --index-url https://download.pytorch.org/whl/cu121

echo "=== INSTALL REQUIREMENTS ==="
pip install -r requirements.txt

echo "=== EXPORT ENV VARS ==="
cat <<EOF >> ~/.bashrc

export MODEL_PATH="/models/base_model/Realistic_Vision_V6.0_NV_B1_fp16.safetensors"
export OUTPUT_DIR="/output"
export LORA_DIR="/models/lora/zootopia.safetensors"
export CONTROLNET_PATH="/models/controlnet/canny"
export GFPGAN_PATH="/models/restoration/GFPGANv1.3.pth"

EOF

source ~/.bashrc

echo "=== LINUX SETUP COMPLETE ==="
