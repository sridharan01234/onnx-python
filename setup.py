#!/usr/bin/env python3
"""
Setup script for ONNX Embedding Server
Installs dependencies and converts the model
"""

import os
import sys
import subprocess
from pathlib import Path

# Fix Windows encoding issue
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')


def run_command(cmd, check=True):
    """Run a command and return the result"""
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, check=check)
    return result.returncode == 0


def install_dependencies():
    """Install Python dependencies"""
    print("📦 Installing dependencies...")
    
    success = run_command([
        sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
    ])
    
    if success:
        print("[OK] Dependencies installed successfully")
    else:
        print("❌ Failed to install dependencies")
    
    return success


def convert_model():
    """Convert the HuggingFace model to ONNX"""
    print("\n🔄 Converting model to ONNX...")
    
    success = run_command([sys.executable, "convert_to_onnx.py"])
    
    if success:
        print("[OK] Model converted successfully")
    else:
        print("❌ Failed to convert model")
    
    return success


def verify_setup():
    """Verify that all files are in place"""
    print("\n🔍 Verifying setup...")
    
    required_files = [
        "onnx_model/model.onnx",
        "tokenizer/tokenizer.json",
        "tokenizer/tokenizer_config.json"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Missing files:")
        for file_path in missing_files:
            print(f"  - {file_path}")
        return False
    
    print("[OK] All required files are present")
    return True


def main():
    """Main setup function"""
    print("🚀 ONNX Embedding Server Setup")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required")
        sys.exit(1)
    
    print(f"[OK] Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Setup failed at dependency installation")
        sys.exit(1)
    
    # Convert model
    if not convert_model():
        print("❌ Setup failed at model conversion")
        sys.exit(1)
    
    # Verify setup
    if not verify_setup():
        print("❌ Setup verification failed")
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("✅ Setup completed successfully!")
    print("\nNext steps:")
    print("1. Run the server: python server.py")
    print("2. Test the API: python test_server.py")
    print("3. Build executables: python build.py")


if __name__ == "__main__":
    main()
