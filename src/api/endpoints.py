from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, Literal
from src.llm_engine.huggingface_provider import HuggingFaceProvider
from src.llm_engine.local_provider import LocalMockProvider
from src.llm_engine.cache import ResponseCache
from src.api.middleware import track_cost, CACHE_EVENTS
import os

router = APIRouter()

# Initialize providers
# In a real app, this might be dependency injected or managed by a factory
hf_provider = HuggingFaceProvider()
local_provider = LocalMockProvider()
response_cache = ResponseCache(ttl_seconds=3600)

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("api")


class GenerateRequest(BaseModel):
    prompt: str
    max_tokens: Optional[int] = 100
    provider: Literal["huggingface", "local", "auto"] = "local"
    model_id: Optional[str] = None # Optional override

@router.post("/generate")
async def generate_text(request: GenerateRequest):
    """
    Generate text. Use 'auto' provider for cost-aware routing.
    """
    # 1. Check Cache
    cached_response = response_cache.get(request.prompt)
    if cached_response:
        CACHE_EVENTS.labels(event_type="hit").inc()
        cached_response["cached"] = True
        return cached_response
    
    CACHE_EVENTS.labels(event_type="miss").inc()

    selected_provider_key = request.provider
    logger.info(f"DEBUG: START Request. Provider requested: {repr(selected_provider_key)}")


    
    # Smart Routing
    if selected_provider_key == "auto":
        from src.llm_engine.router import route_query
        selected_provider_key = route_query(request.prompt)

    if selected_provider_key == "huggingface":
        logger.info("DEBUG: Branch HUGGINGFACE selected")
        provider = hf_provider
        if request.model_id:
             provider.model_id = request.model_id
    elif selected_provider_key == "local":
        provider = local_provider
    else:
        raise HTTPException(status_code=400, detail="Invalid provider")

    print(f"DEBUG: Selected Provider Object: {provider}")
    
    try:
        result = await provider.generate(request.prompt, request.max_tokens)
        
        # Track the cost (Tag with actual used provider)
        track_cost(result["cost"], result.get("model", "unknown"), provider.get_provider_name())
        
        # Add routing breakdown to result for analysis
        result["routed_to"] = selected_provider_key
        result["actual_provider_name"] = provider.get_provider_name()
        result["provider_class"] = str(provider.__class__.__name__)

        # Save to Cache
        response_cache.set(request.prompt, result)
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
def health_check():
    return {"status": "ok"}
