#!/bin/bash

# AWS Test Credentials Setup Script
# This script helps you set up the required GitHub secrets for the CI/CD pipeline

echo "🔧 Setting up AWS Test Credentials for GitHub Actions"
echo "===================================================="
echo ""

echo "You need to add the following GitHub secrets to your repository:"
echo "1. Go to your GitHub repository"
echo "2. Navigate to Settings → Secrets and variables → Actions"
echo "3. Add the following secrets:"
echo ""
echo "These credentials are configured for:"
echo "- S3 Bucket: test-dev-figma-cs"
echo "- AWS Region: eu-north-1"
echo ""
echo "After setting up these secrets, you can:"
echo "1. Push code to trigger builds"
echo "2. Create releases with tags"
echo "3. Download executables from:"
echo "   https://test-dev-figma-cs.s3.eu-north-1.amazonaws.com/onnx-embedding-server/latest/"
echo ""
echo "Note: These are test credentials - use your own for production!"
