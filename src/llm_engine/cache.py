from typing import Dict, Any, Optional
import hashlib
import time

class ResponseCache:
    """
    Simple In-Memory Exact Match Cache.
    In production, this would be Redis/Memcached.
    """
    def __init__(self, ttl_seconds: int = 3600):
        # Key: hash(prompt), Value: (response_dict, timestamp)
        self.store: Dict[str, tuple] = {}
        self.ttl = ttl_seconds
    
    def get_cache_key(self, prompt: str) -> str:
        return hashlib.sha256(prompt.encode()).hexdigest()

    def get(self, prompt: str) -> Optional[Dict[str, Any]]:
        key = self.get_cache_key(prompt)
        if key in self.store:
            data, timestamp = self.store[key]
            if time.time() - timestamp < self.ttl:
                return data
            else:
                del self.store[key]
        return None

    def set(self, prompt: str, response: Dict[str, Any]):
        key = self.get_cache_key(prompt)
        # Store copy to avoid mutation
        self.store[key] = (response, time.time())
