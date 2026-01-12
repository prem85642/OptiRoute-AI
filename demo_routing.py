import requests
import json

BASE_URL = "http://localhost:8000"

def run_demo():
    print("--- Cost-Aware Routing Demo ---\n")

    # Case 1: Short Prompt (Should go to Local)
    short_prompt = "Hello AI"
    print(f"1. Sending Short Prompt: '{short_prompt}'")
    try:
        resp = requests.post(f"{BASE_URL}/generate", json={
            "prompt": short_prompt,
            "provider": "auto",
            "max_tokens": 10
        })
        data = resp.json()
        print(f"   -> Routed To: {data.get('routed_to')}")
        print(f"   -> Cost: ${data.get('cost', 0):.6f}")
        print(f"   -> Response: {data.get('text')}\n")
    except Exception as e:
        print(f"   Error: {e}\n")

    # Case 2: Long Prompt (Should go to Hugging Face)
    long_prompt = "Please explain the socio-economic impacts of the industrial revolution in detail." * 2 # Make it definitely long
    print(f"2. Sending Long Prompt ({len(long_prompt)} chars)...")
    try:
        resp = requests.post(f"{BASE_URL}/generate", json={
            "prompt": long_prompt,
            "provider": "auto",
            "max_tokens": 10
        })
        data = resp.json()
        print(f"   -> Routed To: {data.get('routed_to')}")
        print(f"   -> Actual Provider Name: {data.get('actual_provider_name')}")
        print(f"   -> Provider Class: {data.get('provider_class')}")
        print(f"   -> Cost: ${data.get('cost', 0):.6f}")
        print(f"   -> Response: {data.get('text')}\n")
    except Exception as e:
        print(f"   Error: {e}\n")

if __name__ == "__main__":
    run_demo()
