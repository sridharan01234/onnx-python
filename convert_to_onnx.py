#!/usr/bin/env python3
"""
Convert HuggingFace sentence-transformers model to ONNX format
"""

import os
import sys
from pathlib import Path
from optimum.exporters import onnx
from transformers import AutoTokenizer

# Fix Windows encoding issue
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

def convert_model_to_onnx():
    """Convert sentence-transformers/all-MiniLM-L6-v2 to ONNX"""
    
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    
    # Create directories
    onnx_dir = Path("onnx_model")
    tokenizer_dir = Path("tokenizer")
    onnx_dir.mkdir(exist_ok=True)
    tokenizer_dir.mkdir(exist_ok=True)
    
    print(f"Converting {model_name} to ONNX...")
    
    # Export model to ONNX
    try:
        onnx.main_export(
            model_name_or_path=model_name,
            output=str(onnx_dir),
            task="feature-extraction",
            opset=14,
            optimize="O2",
            device="cpu"
        )
        print(f"[OK] Model exported to {onnx_dir}/model.onnx")
    except Exception as e:
        print(f"Error exporting model: {e}")
        return False
    
    # Save tokenizer locally
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        tokenizer.save_pretrained(str(tokenizer_dir))
        print(f"[OK] Tokenizer saved to {tokenizer_dir}/")
    except Exception as e:
        print(f"Error saving tokenizer: {e}")
        return False
    
    print("[OK] Model conversion completed successfully!")
    return True

if __name__ == "__main__":
    success = convert_model_to_onnx()
    if not success:
        exit(1)
