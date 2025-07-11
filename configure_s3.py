#!/usr/bin/env python3
"""
S3 Configuration Script for ONNX Embedding Server
Helps set up S3 bucket and GitHub secrets for automated builds
"""

import json
import boto3
import sys
from pathlib import Path


def create_s3_bucket(bucket_name='test-dev-figma-cs', region='eu-north-1'):
    """Create S3 bucket for storing executables"""
    try:
        s3_client = boto3.client('s3', region_name=region)
        
        # Create bucket
        if region == 'us-east-1':
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={'LocationConstraint': region}
            )
        
        print(f"✓ Created S3 bucket: {bucket_name}")
        
        # Set public read policy for download URLs
        bucket_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "PublicReadGetObject",
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": "s3:GetObject",
                    "Resource": f"arn:aws:s3:::{bucket_name}/onnx-embedding-server/*"
                }
            ]
        }
        
        s3_client.put_bucket_policy(
            Bucket=bucket_name,
            Policy=json.dumps(bucket_policy)
        )
        
        print(f"✓ Set public read policy for {bucket_name}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating S3 bucket: {e}")
        return False


def generate_download_urls(bucket_name='test-dev-figma-cs', region='eu-north-1'):
    """Generate download URLs for the executables"""
    base_url = f"https://{bucket_name}.s3.{region}.amazonaws.com/onnx-embedding-server"
    
    urls = {
        'latest': {
            'linux': f"{base_url}/latest/embed-server-linux",
            'windows': f"{base_url}/latest/embed-server-win.exe",
            'macos': f"{base_url}/latest/embed-server-macos"
        }
    }
    
    return urls


def update_readme_with_urls(bucket_name='test-dev-figma-cs', region='eu-north-1'):
    """Update README with download URLs"""
    readme_path = Path("README.md")
    
    if not readme_path.exists():
        print("❌ README.md not found")
        return False
    
    # Generate URLs
    urls = generate_download_urls(bucket_name, region)
    
    # Read current README
    with open(readme_path, 'r') as f:
        content = f.read()
    
    # Add download section
    download_section = f"""
## 📥 Download Pre-built Executables

### Latest Release
- **Linux (x64)**: [{urls['latest']['linux']}]({urls['latest']['linux']})
- **Windows (x64)**: [{urls['latest']['windows']}]({urls['latest']['windows']})
- **macOS (x64/ARM64)**: [{urls['latest']['macos']}]({urls['latest']['macos']})

### Usage
```bash
# Linux/macOS
wget {urls['latest']['linux']}
chmod +x embed-server-linux
./embed-server-linux

# Windows
# Download embed-server-win.exe and run it
```

"""
    
    # Insert after the features section
    if "## Features" in content:
        content = content.replace("## Features", download_section + "## Features")
    else:
        # Insert at the beginning
        content = download_section + content
    
    # Write updated README
    with open(readme_path, 'w') as f:
        f.write(content)
    
    print("✓ Updated README.md with download URLs")
    return True


def main():
    """Main configuration function"""
    print("🔧 S3 Configuration for ONNX Embedding Server")
    print("=" * 50)
    
    # Get configuration from user
    bucket_name = input("Enter S3 bucket name (default: test-dev-figma-cs): ").strip() or 'test-dev-figma-cs'
    region = input("Enter AWS region (default: eu-north-1): ").strip() or 'eu-north-1'
    
    if not bucket_name:
        print("❌ Bucket name is required")
        sys.exit(1)
    
    print(f"\nConfiguration:")
    print(f"  Bucket: {bucket_name}")
    print(f"  Region: {region}")
    
    # Create S3 bucket
    if input("\nCreate S3 bucket? (y/n): ").lower() == 'y':
        if create_s3_bucket(bucket_name, region):
            print("✓ S3 bucket created successfully")
        else:
            print("❌ Failed to create S3 bucket")
            sys.exit(1)
    
    # Update GitHub workflow
    workflow_path = Path(".github/workflows/build.yml")
    if workflow_path.exists():
        with open(workflow_path, 'r') as f:
            workflow_content = f.read()
        
        # Update bucket name and region
        workflow_content = workflow_content.replace(
            "S3_BUCKET: 'your-s3-bucket-name'",
            f"S3_BUCKET: '{bucket_name}'"
        )
        workflow_content = workflow_content.replace(
            "AWS_REGION: 'us-east-1'",
            f"AWS_REGION: '{region}'"
        )
        
        with open(workflow_path, 'w') as f:
            f.write(workflow_content)
        
        print("✓ Updated GitHub workflow with S3 configuration")
    
    # Update README
    if input("Update README with download URLs? (y/n): ").lower() == 'y':
        update_readme_with_urls(bucket_name, region)
    
    # Show next steps
    print("\n" + "=" * 50)
    print("✅ Configuration completed!")
    print("\nNext steps:")
    print("1. Add GitHub secrets to your repository:")
    print("   - AWS_ACCESS_KEY_ID_TEST")
    print("   - AWS_SECRET_ACCESS_KEY_TEST")
    print("2. Push code to GitHub to trigger the build")
    print("3. Executables will be uploaded to:")
    print(f"   https://{bucket_name}.s3.{region}.amazonaws.com/onnx-embedding-server/latest/")
    
    # Generate download URLs
    urls = generate_download_urls(bucket_name, region)
    print("\n📥 Download URLs:")
    for platform, url in urls['latest'].items():
        print(f"  {platform}: {url}")


if __name__ == "__main__":
    main()
