# ONNX Embedding Server Makefile

.PHONY: help install convert run test build clean

help:
	@echo "ONNX Embedding Server - Available commands:"
	@echo "  make install    - Install dependencies"
	@echo "  make convert    - Convert model to ONNX"
	@echo "  make setup      - Full setup (install + convert)"
	@echo "  make run        - Run the server"
	@echo "  make test       - Test the server"
	@echo "  make build      - Build executable for current platform"
	@echo "  make build-all  - Build executables for all platforms"
	@echo "  make clean      - Clean build artifacts"

install:
	pip install -r requirements.txt

convert:
	python convert_to_onnx.py

setup:
	python setup.py

run:
	python server.py

test:
	python test_server.py

build:
	python build.py

build-linux:
	python build.py linux

build-windows:
	python build.py windows

build-macos:
	python build.py darwin

build-all: build-linux build-windows build-macos

clean:
	rm -rf build/
	rm -rf onnx_model/
	rm -rf tokenizer/
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -exec rm -rf {} +

# Development targets
dev-install:
	pip install -r requirements.txt
	pip install -e .

lint:
	flake8 *.py
	black --check *.py

format:
	black *.py

# Docker targets
docker-build:
	docker build -t onnx-embedding-server .

docker-run:
	docker run -p 8000:8000 onnx-embedding-server

docker-compose-up:
	docker-compose up -d

docker-compose-down:
	docker-compose down

# S3 and GitHub Actions targets
configure-s3:
	python configure_s3.py

# GitHub Actions will handle building and uploading
# Just push to trigger the build
trigger-build:
	@echo "Push to GitHub to trigger automated build:"
	@echo "  git add ."
	@echo "  git commit -m 'Trigger build'"
	@echo "  git push origin main"
	@echo ""
	@echo "Or create a release:"
	@echo "  git tag v1.0.0"
	@echo "  git push origin v1.0.0"

# Download pre-built executables from S3 (update URLs as needed)
download-executables:
	@echo "Download executables from S3:"
	@echo "Update the URLs in this target after configuring S3"
