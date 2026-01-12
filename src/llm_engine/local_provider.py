import asyncio
import time
import random
from typing import Dict, Any
from .base import LLMProvider

class LocalMockProvider(LLMProvider):
    """
    A Mock provider that simulates a local LLM running on GPU/CPU.
    Useful for baseline testing without incurring API costs or requiring heavy hardware.
    """
    def __init__(self, model_name: str = "llama-2-7b-local"):
        self.model_name = model_name
        # Simulated 'compute' cost per second representing GPU power usage (Real electricity cost is very low)
        self.cost_per_second = 0.000005  # $0.018/hr approx -> negligible

    async def generate(self, prompt: str, max_tokens: int = 100) -> Dict[str, Any]:
        print("DEBUG: Executing LocalMockProvider.generate")
        start_time = time.time()
        
        # Simulate processing time based on token count
        # 0.05s per token generation speed (simulating a decent GPU)
        simulated_latency = 0.5 + (max_tokens * 0.02) 
        await asyncio.sleep(min(simulated_latency, 2.0)) # Cap sleep for development speed
        
        generated_text = f"[MOCK V2] Processed: {prompt[:20]}..."
        
        prompt_tokens = len(prompt) // 4
        completion_tokens = max_tokens
        total_tokens = prompt_tokens + completion_tokens
        
        end_time = time.time()
        actual_latency = end_time - start_time
        
        # Local cost is time-based (GPU uptime), not token-based
        cost = actual_latency * self.cost_per_second

        return {
            "text": generated_text,
            "usage": {
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "total_tokens": total_tokens
            },
            "cost": cost,
            "latency": actual_latency,
            "model": self.model_name
        }

    def get_provider_name(self) -> str:
        return "local_mock_gpu"
