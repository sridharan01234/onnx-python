#!/usr/bin/env python3
"""
Quick test to verify all components are working
"""

import sys
import os
from pathlib import Path

# Fix Windows encoding issue
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

def test_imports():
    """Test that all required modules can be imported"""
    print("[TEST] Testing imports...")
    
    try:
        import numpy as np
        print("[OK] numpy imported")
    except ImportError as e:
        print(f"[FAIL] numpy import failed: {e}")
        return False
    
    try:
        import onnxruntime as ort
        print("[OK] onnxruntime imported")
    except ImportError as e:
        print(f"[FAIL] onnxruntime import failed: {e}")
        return False
    
    try:
        import transformers
        print("[OK] transformers imported")
    except ImportError as e:
        print(f"[FAIL] transformers import failed: {e}")
        return False
    
    try:
        import fastapi
        print("[OK] fastapi imported")
    except ImportError as e:
        print(f"[FAIL] fastapi import failed: {e}")
        return False
    
    try:
        import nuitka
        print("[OK] nuitka imported")
    except ImportError as e:
        print(f"[FAIL] nuitka import failed: {e}")
        return False
    
    return True

def test_file_structure():
    """Test that required files exist"""
    print("[TEST] Testing file structure...")
    
    required_files = [
        "server.py",
        "convert_to_onnx.py",
        "build.py",
        "requirements.txt"
    ]
    
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"[OK] {file_path} exists")
        else:
            print(f"[FAIL] {file_path} missing")
            return False
    
    return True

def main():
    """Main test function"""
    print("[TEST] Quick Setup Verification")
    print("=" * 50)
    
    print(f"Python version: {sys.version}")
    print(f"Platform: {sys.platform}")
    print(f"Working directory: {os.getcwd()}")
    print()
    
    # Test imports
    if not test_imports():
        print("[FAIL] Import tests failed")
        return False
    
    print()
    
    # Test file structure
    if not test_file_structure():
        print("[FAIL] File structure tests failed")
        return False
    
    print()
    print("[OK] All tests passed!")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
