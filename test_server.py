#!/usr/bin/env python3
"""
Test script for the ONNX embedding server
"""

import requests
import json
import time
import sys


def test_server(base_url="http://localhost:8000"):
    """Test the embedding server"""
    
    print("🧪 Testing ONNX Embedding Server")
    print("=" * 40)
    
    # Test health endpoint
    try:
        print("Testing health endpoint...")
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            health_data = response.json()
            print(f"✓ Health check: {health_data}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to server: {e}")
        print("Make sure the server is running on localhost:8000")
        return False
    
    # Test embedding endpoint
    test_texts = [
        "Hello world!",
        "This is a test sentence for embedding.",
        "Machine learning is awesome!",
        "ONNX Runtime provides fast inference.",
        ""  # Empty text to test error handling
    ]
    
    for i, text in enumerate(test_texts):
        print(f"\nTest {i+1}: '{text}'")
        
        try:
            response = requests.post(
                f"{base_url}/embed",
                json={"text": text},
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                embedding = data["embedding"]
                dimension = data["dimension"]
                print(f"✓ Success: {dimension}D embedding")
                print(f"  First 5 values: {embedding[:5]}")
                print(f"  Embedding norm: {sum(x*x for x in embedding)**0.5:.4f}")
            else:
                print(f"❌ Failed: {response.status_code}")
                print(f"  Error: {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Request failed: {e}")
    
    print("\n" + "=" * 40)
    print("✓ Test completed!")
    return True


def benchmark_server(base_url="http://localhost:8000", num_requests=10):
    """Benchmark the server performance"""
    
    print(f"\n🏃 Benchmarking server ({num_requests} requests)")
    print("=" * 40)
    
    test_text = "This is a benchmark test for the embedding server performance."
    
    times = []
    for i in range(num_requests):
        start_time = time.time()
        
        try:
            response = requests.post(
                f"{base_url}/embed",
                json={"text": test_text},
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                end_time = time.time()
                times.append(end_time - start_time)
                print(f"Request {i+1}: {(end_time - start_time)*1000:.1f}ms")
            else:
                print(f"Request {i+1}: Failed ({response.status_code})")
                
        except requests.exceptions.RequestException as e:
            print(f"Request {i+1}: Error - {e}")
    
    if times:
        avg_time = sum(times) / len(times)
        min_time = min(times)
        max_time = max(times)
        
        print(f"\nPerformance Summary:")
        print(f"  Average: {avg_time*1000:.1f}ms")
        print(f"  Min: {min_time*1000:.1f}ms")
        print(f"  Max: {max_time*1000:.1f}ms")
        print(f"  Requests/sec: {1/avg_time:.1f}")


def main():
    """Main test function"""
    
    # Check if server URL is provided
    base_url = "http://localhost:8000"
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    
    print(f"Testing server at: {base_url}")
    
    # Run tests
    success = test_server(base_url)
    
    if success:
        # Run benchmark
        benchmark_server(base_url)
    
    print("\n🎯 Test script completed!")


if __name__ == "__main__":
    main()
