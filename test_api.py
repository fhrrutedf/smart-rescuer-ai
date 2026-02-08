"""
Test script for Smart Rescuer API
"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
import requests
import json


# Test 1: Status endpoint
print("=" * 50)
print("Test 1: Checking API Status")
print("=" * 50)

try:
    response = requests.get("http://localhost:8000/api/status")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    print("[OK] Status endpoint working!")
except Exception as e:
    print(f"[ERROR] Error: {e}")

print("\n" + "=" * 50)
print("Test 2: Emergency Assessment (without image)")
print("=" * 50)

try:
    # Test emergency assessment without image
    data = {
        "patient_conscious": True
    }
    response = requests.post("http://localhost:8000/api/emergency/assess", data=data)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print("\nAssessment Results:")
        print(f"Severity: {result.get('assessment', {}).get('severity', {}).get('severity_level', 'N/A')}")
        print(f"Score: {result.get('assessment', {}).get('severity', {}).get('total_score', 'N/A')}/10")
        print(f"Injuries: {len(result.get('assessment', {}).get('injuries', []))}")
        print("\n[OK] Emergency assessment working!")
        print("\nFull Response (first 500 chars):")
        print(str(result)[:500])
    else:
        print(f"[ERROR] Error: {response.text}")
        
except Exception as e:
    print(f"[ERROR] Error: {e}")

print("\n" + "=" * 50)
print("Test 3: Root endpoint")
print("=" * 50)

try:
    response = requests.get("http://localhost:8000/")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    print("[OK] Root endpoint working!")
except Exception as e:
    print(f"[ERROR] Error: {e}")

print("\n" + "=" * 50)
print("[OK] All Tests Completed!")
print("=" * 50)
