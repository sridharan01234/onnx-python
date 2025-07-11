#!/usr/bin/env python3
"""
FastAPI ONNX Embedding Server
Serves embeddings from a local ONNX model without internet access
"""

import os
import sys
from pathlib import Path
from typing import Dict, List
import json
import numpy as np
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import onnxruntime as ort
from transformers import AutoTokenizer

# Fix Windows encoding issue
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')


class EmbedRequest(BaseModel):
    text: str


class EmbedResponse(BaseModel):
    embedding: List[float]
    dimension: int


class ONNXEmbeddingServer:
    def __init__(self):
        self.tokenizer = None
        self.onnx_session = None
        self.model_max_length = 512
        
    def load_model(self):
        """Load tokenizer and ONNX model"""
        # Get the directory of the current script
        if getattr(sys, 'frozen', False):
            # If running as a Nuitka executable
            base_dir = Path(sys.executable).parent
        else:
            # If running as a Python script
            base_dir = Path(__file__).parent
        
        tokenizer_path = base_dir / "tokenizer"
        model_path = base_dir / "onnx_model" / "model.onnx"
        
        print(f"Loading tokenizer from: {tokenizer_path}")
        print(f"Loading model from: {model_path}")
        
        # Check if files exist
        if not tokenizer_path.exists():
            raise FileNotFoundError(f"Tokenizer directory not found: {tokenizer_path}")
        if not model_path.exists():
            raise FileNotFoundError(f"ONNX model not found: {model_path}")
        
        # Load tokenizer
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(
                str(tokenizer_path),
                local_files_only=True
            )
            print("[OK] Tokenizer loaded successfully")
        except Exception as e:
            raise RuntimeError(f"Failed to load tokenizer: {e}")
        
        # Load ONNX model
        try:
            providers = ['CPUExecutionProvider']
            self.onnx_session = ort.InferenceSession(
                str(model_path),
                providers=providers
            )
            print("[OK] ONNX model loaded successfully")
        except Exception as e:
            raise RuntimeError(f"Failed to load ONNX model: {e}")
    
    def mean_pooling(self, model_output, attention_mask):
        """Apply mean pooling to get sentence embeddings"""
        token_embeddings = model_output[0]  # First element contains all token embeddings
        input_mask_expanded = np.expand_dims(attention_mask, axis=-1)
        input_mask_expanded = np.broadcast_to(input_mask_expanded, token_embeddings.shape).astype(np.float32)
        
        # Sum embeddings and mask
        sum_embeddings = np.sum(token_embeddings * input_mask_expanded, axis=1)
        sum_mask = np.sum(input_mask_expanded, axis=1)
        
        # Avoid division by zero
        sum_mask = np.clip(sum_mask, a_min=1e-9, a_max=None)
        
        # Calculate mean
        mean_embeddings = sum_embeddings / sum_mask
        return mean_embeddings
    
    def embed_text(self, text: str) -> List[float]:
        """Generate embeddings for input text"""
        if not self.tokenizer or not self.onnx_session:
            raise RuntimeError("Model not loaded. Call load_model() first.")
        
        # Tokenize
        encoded = self.tokenizer(
            text,
            padding=True,
            truncation=True,
            max_length=self.model_max_length,
            return_tensors="np"
        )
        
        # Prepare inputs for ONNX
        onnx_inputs = {
            "input_ids": encoded["input_ids"].astype(np.int64),
            "attention_mask": encoded["attention_mask"].astype(np.int64),
        }
        
        # Add token_type_ids if present
        if "token_type_ids" in encoded:
            onnx_inputs["token_type_ids"] = encoded["token_type_ids"].astype(np.int64)
        
        # Run inference
        outputs = self.onnx_session.run(None, onnx_inputs)
        
        # Apply mean pooling
        embeddings = self.mean_pooling(outputs, encoded["attention_mask"])
        
        # Normalize embeddings
        embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)
        
        return embeddings[0].tolist()


# Global server instance
embedding_server = ONNXEmbeddingServer()

# FastAPI app
app = FastAPI(
    title="ONNX Embedding Server",
    description="Standalone embedding server using ONNX Runtime",
    version="1.0.0"
)


@app.on_event("startup")
async def startup_event():
    """Initialize the embedding server on startup"""
    print("Starting ONNX Embedding Server...")
    try:
        embedding_server.load_model()
        print("[OK] Server ready!")
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        raise


@app.get("/")
async def root():
    return {"message": "ONNX Embedding Server is running"}


@app.get("/health")
async def health_check():
    return {"status": "healthy", "model_loaded": embedding_server.onnx_session is not None}


@app.post("/embed", response_model=EmbedResponse)
async def embed_text(request: EmbedRequest):
    """Generate embeddings for input text"""
    try:
        if not request.text.strip():
            raise HTTPException(status_code=400, detail="Text cannot be empty")
        
        embedding = embedding_server.embed_text(request.text)
        
        return EmbedResponse(
            embedding=embedding,
            dimension=len(embedding)
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating embedding: {str(e)}")


def main():
    """Main entry point for the server"""
    print("🚀 Starting ONNX Embedding Server...")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )


if __name__ == "__main__":
    main()
