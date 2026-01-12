from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class LLMProvider(ABC):
    """
    Abstract base class for LLM providers.
    Enforces a consistent interface for generating text and tracking costs.
    """

    @abstractmethod
    async def generate(self, prompt: str, max_tokens: int = 100) -> Dict[str, Any]:
        """
        Generate text based on the prompt.
        
        Args:
            prompt (str): The input text.
            max_tokens (int): Maximum generation length.

        Returns:
            Dict[str, Any]: A dictionary containing:
                - text: The generated text.
                - usage: Token usage stats (prompt_tokens, completion_tokens, total_tokens).
                - cost: Estimated cost for this call.
                - latency: Time taken for the call.
        """
        pass

    @abstractmethod
    def get_provider_name(self) -> str:
        """Returns the name of the provider."""
        pass
