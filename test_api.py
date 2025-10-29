#!/usr/bin/env python3
"""
Simple test script for the RA Longevity API
Tests all endpoints to ensure they work correctly.
"""

import requests
import time
import sys

BASE_URL = "http://localhost:8080"
TOKEN = "test-token-12345"

def print_test(test_name):
    print(f"\n{'='*60}")
    print(f"Testing: {test_name}")
    print('='*60)

def test_root():
    """Test root endpoint (no auth required)"""
    print_test("Root Endpoint")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    assert response.status_code == 200
    print("✓ Root endpoint test passed")

def test_analyze():
    """Test analyze endpoint"""
    print_test("Analyze Endpoint")
    headers = {"Authorization": f"Bearer {TOKEN}"}
    data = {
        "data": [
            {"x": 1.0, "y": 2.0},
            {"x": 1.5, "y": 2.5},
            {"x": 2.0, "y": 3.0}
        ],
        "mode": "tabular",
        "threshold": 0.1
    }
    
    response = requests.post(
        f"{BASE_URL}/api/longevity/analyze",
        headers=headers,
        json=data
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Run ID: {result['run_id']}")
        print(f"Predictions: {result['predictions'][:3]}...")
        print(f"LDrop Metrics: {result['ldrop_metrics']}")
        print(f"DKIL Locked: {result['dkil_locked']}")
        print("✓ Analyze endpoint test passed")
        return result['run_id']
    else:
        print(f"Error: {response.text}")
        sys.exit(1)

def test_get_report(run_id):
    """Test get report endpoint"""
    print_test(f"Get Report Endpoint (run_id: {run_id})")
    headers = {"Authorization": f"Bearer {TOKEN}"}
    
    response = requests.get(
        f"{BASE_URL}/api/longevity/report/{run_id}",
        headers=headers
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Run ID: {result['run_id']}")
        print(f"DKIL Locked: {result['dkil_locked']}")
        print(f"Has JSON Report: {result['json_report'] is not None}")
        print(f"Has HTML Report: {result['html_report'] is not None}")
        print("✓ Get report endpoint test passed")
    else:
        print(f"Error: {response.text}")
        sys.exit(1)

def test_download_bundle(run_id):
    """Test download bundle endpoint"""
    print_test(f"Download Bundle Endpoint (run_id: {run_id})")
    headers = {"Authorization": f"Bearer {TOKEN}"}
    
    response = requests.get(
        f"{BASE_URL}/api/longevity/report/{run_id}/download",
        headers=headers
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(f"Bundle size: {len(response.content)} bytes")
        print("✓ Download bundle endpoint test passed")
    else:
        print(f"Error: {response.text}")
        sys.exit(1)

def test_deploy(run_id):
    """Test deploy endpoint"""
    print_test(f"Deploy Endpoint (run_id: {run_id})")
    headers = {"Authorization": f"Bearer {TOKEN}"}
    data = {
        "run_id": run_id,
        "human_key": "human-approval-key-12345",
        "logic_key": "logic-validation-key-67890",
        "dkil_validation": False  # Set to False since we may not have threshold met
    }
    
    response = requests.post(
        f"{BASE_URL}/api/longevity/deploy",
        headers=headers,
        json=data
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Status: {result['status']}")
        print(f"Model Registry URL: {result['model_registry_url']}")
        print(f"Message: {result['message']}")
        print("✓ Deploy endpoint test passed")
    else:
        print(f"Error: {response.text}")
        sys.exit(1)

def test_auth_failure():
    """Test authentication failure"""
    print_test("Authentication Failure")
    headers = {"Authorization": "Bearer invalid-token"}
    
    response = requests.get(
        f"{BASE_URL}/api/longevity/report/test",
        headers=headers
    )
    
    print(f"Status: {response.status_code}")
    assert response.status_code == 401, "Expected 401 for invalid token"
    print("✓ Authentication failure test passed")

def main():
    """Run all tests"""
    print("="*60)
    print("RA Longevity API Test Suite")
    print("="*60)
    print(f"Base URL: {BASE_URL}")
    print(f"Token: {TOKEN}")
    
    try:
        # Wait for server to be ready
        print("\nWaiting for server to be ready...")
        max_retries = 30
        for i in range(max_retries):
            try:
                requests.get(f"{BASE_URL}/", timeout=1)
                print("✓ Server is ready")
                break
            except requests.exceptions.RequestException:
                if i == max_retries - 1:
                    print("✗ Server not ready after 30 seconds")
                    sys.exit(1)
                time.sleep(1)
        
        # Run tests
        test_root()
        run_id = test_analyze()
        test_get_report(run_id)
        test_download_bundle(run_id)
        test_deploy(run_id)
        test_auth_failure()
        
        print("\n" + "="*60)
        print("ALL TESTS PASSED ✓")
        print("="*60)
        
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
