import requests
import time

def test_api():
    base_url = "http://localhost:8000"
    
    print("Checking health...")
    try:
        resp = requests.get(f"{base_url}/health")
        print(f"Health: {resp.status_code} - {resp.json()}")
    except Exception as e:
        print(f"Health Check Failed: {e}")
        return

    print("\nTesting Local Generation...")
    try:
        start = time.time()
        resp = requests.post(f"{base_url}/generate", json={
            "prompt": "Test prompt",
            "max_tokens": 10,
            "provider": "local"
        })
        print(f"Local status: {resp.status_code}")
        print(f"Local Output: {resp.json()}")
        print(f"Time: {time.time() - start:.2f}s")
    except Exception as e:
        print(f"Local Gen Failed: {e}")

    # Uncomment to test HF if token is valid and you want to spend fake credits/wait
    # print("\nTesting HF Generation...")
    # try:
    #     resp = requests.post(f"{base_url}/generate", json={
    #         "prompt": "Say hello",
    #         "max_tokens": 5,
    #         "provider": "huggingface"
    #     })
    #     print(f"HF status: {resp.status_code}")
    #     print(f"HF Output: {resp.json()}")
    # except Exception as e:
    #     print(f"HF Gen Failed: {e}")

if __name__ == "__main__":
    test_api()
