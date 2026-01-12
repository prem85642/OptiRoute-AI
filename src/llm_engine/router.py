from typing import Literal

def route_query(prompt: str) -> Literal["local", "huggingface"]:
    """
    Decides which provider to use based on prompt complexity.
    
    Strategy:
    - 'local': Cheap, fast, good for simple/short queries.
    - 'huggingface': More capable, costs money, good for complex tasks.
    
    Heuristic:
    - If prompt length > 60 chars, assume it's complex -> HF.
    - Else -> Local.
    """
    # Simple length-based heuristic for demonstration
    if len(prompt) > 60:
        return "huggingface"
    return "local"
