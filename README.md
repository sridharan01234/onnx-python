# ONNX Embedding Server

A standalone, cross-platform embedding server that runs entirely offline using ONNX Runtime and FastAPI.

## Features

- 🚀 **Standalone executables** - Single binary files for Linux, Windows, and macOS
- 🌐 **No internet required** - All model files bundled into the executable
- ⚡ **Fast inference** - Uses ONNX Runtime for optimized performance
- 🔌 **Simple API** - RESTful API with FastAPI
- 📦 **Small model** - Uses `sentence-transformers/all-MiniLM-L6-v2` (22MB)

## Quick Start

### Option 1: Run Pre-built Executable

#### Download from GitHub Releases
1. Go to the [Releases](../../releases) page
2. Download the appropriate executable for your platform:
   - `embed-server-linux` (Linux x64)
   - `embed-server-win.exe` (Windows x64)
   - `embed-server-macos` (macOS x64/ARM64)

#### Download from S3 (Test Environment)
```bash
# Linux
wget https://test-dev-figma-cs.s3.eu-north-1.amazonaws.com/onnx-embedding-server/latest/embed-server-linux
chmod +x embed-server-linux
./embed-server-linux

# Windows - Download and run
# https://test-dev-figma-cs.s3.eu-north-1.amazonaws.com/onnx-embedding-server/latest/embed-server-win.exe

# macOS
wget https://test-dev-figma-cs.s3.eu-north-1.amazonaws.com/onnx-embedding-server/latest/embed-server-macos
chmod +x embed-server-macos
./embed-server-macos
```

#### Run the Server
```bash
# Linux/macOS
./embed-server-linux

# Windows
embed-server-win.exe
```

#### Test the API
```bash
curl -X POST http://localhost:8000/embed \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello world!"}'
```

### Option 2: Build from Source

#### Prerequisites

- Python 3.8+
- pip

#### Installation

1. Clone and setup:
   ```bash
   git clone <repository>
   cd onnx-python
   pip install -r requirements.txt
   ```

2. Convert the model to ONNX:
   ```bash
   python convert_to_onnx.py
   ```

3. Run the server directly:
   ```bash
   python server.py
   ```

#### Building Executables

Build for your current platform:
```bash
python build.py
```

Build for a specific platform:
```bash
python build.py linux    # Build for Linux
python build.py windows  # Build for Windows  
python build.py darwin   # Build for macOS
```

Executables will be created in the `build/` directory.

## 🚀 Automated Builds (Recommended)

For faster builds without straining your local machine, use GitHub Actions:

### Setup
1. **Configure S3 bucket**: `python configure_s3.py`
2. **Add GitHub secrets**: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`
3. **Push to trigger build**: `git push origin main`

### What You Get
- ✅ Multi-platform builds (Linux, Windows, macOS)
- ✅ Automatic testing of each executable
- ✅ S3 upload for easy distribution
- ✅ GitHub releases for version management
- ✅ No local resource usage

See [GITHUB_ACTIONS_SETUP.md](GITHUB_ACTIONS_SETUP.md) for detailed setup instructions.

## API Documentation

### POST `/embed`

Generate embeddings for input text.

**Request:**
```json
{
  "text": "Your text to embed"
}
```

**Response:**
```json
{
  "embedding": [0.1, 0.2, -0.3, ...],
  "dimension": 384
}
```

### GET `/health`

Check server health status.

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true
}
```

## Project Structure

```
onnx-python/
├── server.py              # FastAPI server
├── convert_to_onnx.py     # Model conversion script
├── build.py               # Build script for executables
├── requirements.txt       # Python dependencies
├── onnx_model/
│   └── model.onnx        # ONNX model file
├── tokenizer/            # Tokenizer files
│   ├── tokenizer.json
│   ├── tokenizer_config.json
│   └── ...
└── build/                # Built executables
    ├── embed-server-linux
    ├── embed-server-win.exe
    └── embed-server-macos
```

## Technical Details

### Model Information

- **Base Model**: `sentence-transformers/all-MiniLM-L6-v2`
- **Embedding Dimensions**: 384
- **Max Sequence Length**: 512 tokens
- **Model Size**: ~22MB
- **Inference Provider**: CPU (ONNX Runtime)

### Performance

- **Startup Time**: ~2-3 seconds
- **Inference Speed**: ~50-100ms per embedding (CPU)
- **Memory Usage**: ~150MB RAM
- **Binary Size**: ~80-120MB (depending on platform)

### Security

- **No Network Access**: All files bundled, no internet required
- **Local Only**: Server binds to localhost by default
- **No Data Persistence**: No logs or data stored locally

## Development

### Running Tests

```bash
# Start server
python server.py

# Test endpoint
curl -X POST http://localhost:8000/embed \
  -H "Content-Type: application/json" \
  -d '{"text": "Test embedding"}'
```

### Debugging

To enable console output in the built executable, modify `build.py`:

```python
# Remove this line:
"--disable-console",
```

### Custom Models

To use a different model:

1. Modify `convert_to_onnx.py` to use your model
2. Ensure the model is compatible with `feature-extraction` task
3. Update the tokenizer loading in `server.py` if needed

## Troubleshooting

### Common Issues

1. **"Model not found" error**:
   - Run `python convert_to_onnx.py` first
   - Check that `onnx_model/model.onnx` exists

2. **"Tokenizer not found" error**:
   - Ensure `tokenizer/` directory exists with required files
   - Check that `tokenizer.json` is present

3. **Build fails**:
   - Install all requirements: `pip install -r requirements.txt`
   - Check Python version (3.8+ required)
   - Ensure Nuitka is installed

4. **Large binary size**:
   - This is normal for bundled ML models
   - Use `--onefile` for single executable
   - Consider model quantization for smaller size

### Platform-Specific Notes

- **Linux**: Requires glibc 2.17+ (CentOS 7+, Ubuntu 14.04+)
- **Windows**: Requires Windows 10+ (64-bit)
- **macOS**: Requires macOS 10.14+ (supports both Intel and Apple Silicon)

## License

This project is open source. Check individual model licenses for usage restrictions.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Support

For issues and questions:
- Check the troubleshooting section above
- Review the server logs for error details
- Ensure all dependencies are correctly installed
