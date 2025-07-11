#!/usr/bin/env python3
"""
Build script for creating cross-platform executables using Nuitka
"""

import os
import sys
import shutil
import platform
from pathlib import Path
import subprocess


def run_command(cmd, check=True):
    """Run a command and return the result"""
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, check=check, capture_output=True, text=True)
    if result.stdout:
        print("STDOUT:", result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    if result.returncode != 0:
        print(f"Command failed with return code: {result.returncode}")
    return result


def build_executable(target_os=None):
    """Build executable for the specified OS"""
    
    # Create build directory
    build_dir = Path("build")
    build_dir.mkdir(exist_ok=True)
    
    # Determine current and target OS
    current_os = platform.system().lower()
    if target_os:
        target_os = target_os.lower()
    else:
        target_os = current_os
    
    # Base Nuitka command
    base_cmd = [
        sys.executable, "-m", "nuitka",
        "--onefile",
        "--standalone",
        "--follow-imports",
        "--output-dir=build",
    ]
    
    # Add platform-specific options
    if current_os == "windows":
        base_cmd.extend([
            "--disable-console",
            "--windows-disable-console",
        ])
    # For Linux and macOS, keep console enabled for debugging
    
    # Add data files (model and tokenizer)
    data_files = [
        "--include-data-dir=onnx_model=onnx_model",
        "--include-data-dir=tokenizer=tokenizer",
    ]
    
    # Determine output name based on OS
    current_os = platform.system().lower()
    if target_os:
        target_os = target_os.lower()
    else:
        target_os = current_os
    
    # Map OS names correctly
    if target_os == "windows":
        output_name = "embed-server-win.exe"
    elif target_os == "macos" or target_os == "darwin":
        output_name = "embed-server-macos"
    elif target_os == "linux":
        output_name = "embed-server-linux"
    else:
        # Auto-detect based on current platform
        if current_os == "windows":
            output_name = "embed-server-win.exe"
        elif current_os == "darwin":
            output_name = "embed-server-macos"
        else:  # linux
            output_name = "embed-server-linux"
    
    # Build command
    cmd = base_cmd + data_files + [
        f"--output-filename={output_name}",
        "server.py"
    ]
    
    print(f"Building executable for {target_os} (current OS: {current_os})...")
    print(f"Output name: {output_name}")
    print("This may take several minutes...")
    
    try:
        result = run_command(cmd)
        print(f"✓ Successfully built {output_name}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        print(f"Command that failed: {' '.join(cmd)}")
        return False


def verify_requirements():
    """Verify that required files exist"""
    required_files = [
        "server.py",
        "onnx_model/model.onnx",
        "tokenizer/tokenizer.json",
        "tokenizer/tokenizer_config.json"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Missing required files:")
        for file_path in missing_files:
            print(f"  - {file_path}")
        print("\nPlease run 'python convert_to_onnx.py' first to generate the model files.")
        return False
    
    return True


def main():
    """Main build function"""
    print("🔨 ONNX Embedding Server Build Script")
    print("=" * 50)
    
    # Check requirements
    if not verify_requirements():
        sys.exit(1)
    
    # Get target OS from command line
    target_os = None
    if len(sys.argv) > 1:
        target_os = sys.argv[1]
    
    # Build executable
    success = build_executable(target_os)
    
    if success:
        print("✓ Build completed successfully!")
        print(f"Executable is in the build/ directory")
        
        # List built files
        build_dir = Path("build")
        if build_dir.exists():
            print("\nBuilt files:")
            for file in build_dir.iterdir():
                if file.is_file() and file.suffix in ['.exe', ''] and 'embed-server' in file.name:
                    print(f"  - {file}")
    else:
        print("❌ Build failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
