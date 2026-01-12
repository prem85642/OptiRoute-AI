import asyncio
import os
import httpx
from typing import Dict, Any
from .base import LLMProvider

class HuggingFaceProvider(LLMProvider):
    """
    Provider for Hugging Face Inference API (Async + Circuit Breaker).
    """
    def __init__(self, model_id: str = "mistralai/Mistral-7B-Instruct-v0.2"):
        self.api_token = os.getenv("HF_API_TOKEN")
        self.model_id = model_id
        self.input_cost_per_1k = 0.0002
        self.output_cost_per_1k = 0.0002
        
        # Circuit Breaker State
        self.failure_count = 0
        self.failure_threshold = 3
        self.circuit_open_until = 0  # Timestamp when circuit closes
        self.circuit_timeout_seconds = 30 # How long to stay in fallback mode

    async def generate(self, prompt: str, max_tokens: int = 100) -> Dict[str, Any]:
        # circuit breaker check
        if self.is_circuit_open():
            print("DEBUG: Circuit OPEN. Using Fast Fallback.")
            return await self.fallback_generate(prompt, max_tokens, reason="CircuitOpen")

        print("DEBUG: Executing HuggingFaceProvider.generate (Async)")
        start_time = asyncio.get_running_loop().time()
        
        headers = {"Authorization": f"Bearer {self.api_token}"}
        payload = {
            "inputs": prompt,
            "parameters": {"max_new_tokens": max_tokens, "return_full_text": False, "details": True}
        }
        api_url = f"https://api-inference.huggingface.co/models/{self.model_id}"

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(api_url, json=payload, headers=headers)
                response.raise_for_status()
                data = response.json()
                
                # HF returns a list [0]
                if isinstance(data, list) and len(data) > 0:
                    result = data[0]
                else:
                    result = data

                generated_text = result.get("generated_text", "")
                details = result.get("details", {})
                
                # Success -> Reset Circuit
                self.failure_count = 0
                
                completion_tokens = details.get("generated_tokens", len(generated_text) // 4)
                prompt_tokens = len(prompt) // 4
                
                cost = (prompt_tokens / 1000 * self.input_cost_per_1k) + \
                       (completion_tokens / 1000 * self.output_cost_per_1k)
                
                latency = asyncio.get_running_loop().time() - start_time
                
                return {
                    "text": generated_text,
                    "usage": {"prompt_tokens": prompt_tokens, "completion_tokens": completion_tokens},
                    "cost": cost,
                    "latency": latency,
                    "model": self.model_id
                }

        except Exception as e:
            print(f"DEBUG: HF API Async Fail ({e}). Triggering Circuit Breaker.")
            self.record_failure()
            return await self.fallback_generate(prompt, max_tokens, reason=str(e))

    def is_circuit_open(self) -> bool:
        if self.circuit_open_until > asyncio.get_running_loop().time():
            return True
        if self.failure_count >= self.failure_threshold:
            # Trip the circuit
            self.circuit_open_until = asyncio.get_running_loop().time() + self.circuit_timeout_seconds
            return True
        return False

    def record_failure(self):
        self.failure_count += 1
    
    async def fallback_generate(self, prompt: str, max_tokens: int, reason: str) -> Dict[str, Any]:
        """Async Fallback Provider (Simulation)"""
        start_time = asyncio.get_running_loop().time()
        
        # Simulate network latency (Non-blocking!)
        await asyncio.sleep(2.0)
        
        generated_text = f"[HF FALLBACK - {reason[:20]}...] {prompt[:40]}... (Simulated Response)"
        
        prompt_tokens = len(prompt) // 4
        completion_tokens = 50
        cost = (prompt_tokens / 1000 * self.input_cost_per_1k) + \
               (completion_tokens / 1000 * self.output_cost_per_1k)
        
        return {
            "text": generated_text,
            "usage": {"prompt_tokens": prompt_tokens, "completion_tokens": completion_tokens},
            "cost": cost,
            "latency": asyncio.get_running_loop().time() - start_time,
            "model": f"{self.model_id} (Simulated)"
        }

    def get_provider_name(self) -> str:
        return "huggingface_api"
