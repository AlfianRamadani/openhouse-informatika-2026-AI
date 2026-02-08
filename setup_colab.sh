

echo "=== UPDATE SYSTEM ==="
apt update
apt install -y libgl1 ffmpeg git wget

echo "=== UPGRADE PIP ==="
pip install --upgrade pip setuptools wheel

echo "=== INSTALL TORCH CUDA ==="
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

echo "=== INSTALL REQUIREMENTS ==="
pip install -r requirements.txt

echo "=== DONE ==="
echo "Silakan jalankan Python cell untuk mount Drive dan set environment variables"
