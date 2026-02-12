import os
from pathlib import Path

import torch

ROOT_DIR = Path(__file__).resolve().parents[1]

def check_env_path(name, must_exist=True):
    value = os.getenv(name)
    if not value:
        return (False, f"{name} is not set")
    path = Path(value)
    if must_exist and not path.exists():
        return (False, f"{name} path not found: {value}")
    return (True, f"{name} OK: {value}")

def main():
    print("== Health Check ==")
    print(f"Project root: {ROOT_DIR}")

    # GPU
    if torch.cuda.is_available():
        device_name = torch.cuda.get_device_name(0)
        print(f"GPU OK: {device_name}")
    else:
        print("GPU NOT FOUND: CUDA is not available")

    # Model paths
    checks = [
        check_env_path("MODEL_PATH"),
        check_env_path("CONTROLNET_PATH"),
        check_env_path("GFPGAN_PATH"),
    ]

    lora_keys = ["LORA_ANIME", "LORA_GHIBLI", "LORA_ZOOTOPIA"]
    if any(os.getenv(key) for key in lora_keys):
        for key in lora_keys:
            checks.append(check_env_path(key))
    else:
        checks.append(check_env_path("LORA_DIR"))

    for ok, msg in checks:
        status = "OK" if ok else "FAIL"
        print(f"{status}: {msg}")

    # OUTPUT_DIR
    output_dir = os.getenv("OUTPUT_DIR") or str(ROOT_DIR / "outputs")
    try:
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        print(f"OK: OUTPUT_DIR writable at {output_dir}")
    except Exception as e:
        print(f"FAIL: OUTPUT_DIR not writable at {output_dir} ({e})")

if __name__ == "__main__":
    main()
