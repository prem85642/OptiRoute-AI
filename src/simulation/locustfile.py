from locust import HttpUser, task, between, events
import random

class LLMUser(HttpUser):
    wait_time = between(1, 4) # Users wait 1-4 seconds between requests

    @task(3)
    def generate_short_local(self):
        """Simulate a common, cheap local request."""
        self.client.post("/generate", json={
            "prompt": "Hello",
            "max_tokens": 10,
            "provider": "auto" # Should route to local
        }, name="/generate (auto-short)")

    @task(1)
    def generate_complex_hf(self):
        """Simulate a complex, expensive HF API request."""
        self.client.post("/generate", json={
            "prompt": "Write a detailed explanation of quantum computing and its effects on cryptography.", # Long prompt
            "max_tokens": 50,
            "provider": "auto" # Should route to HF
        }, name="/generate (auto-complex)")

    def on_start(self):
        pass

# Hook for custom stats if needed
@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    print("Starting load test...")
