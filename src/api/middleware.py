import time
from fastapi import Request
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

# Prometheus Metrics
REQUEST_COUNT = Counter("http_requests_total", "Total HTTP requests", ["method", "endpoint", "status"])
REQUEST_LATENCY = Histogram("http_request_duration_seconds", "HTTP request latency", ["method", "endpoint"])
TOTAL_COST = Counter("llm_total_cost_usd", "Total estimated cost in USD", ["model", "provider"])
CACHE_EVENTS = Counter("llm_cache_events_total", "Cache hits and misses", ["event_type"])

class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        response = await call_next(request)
        
        process_time = time.time() - start_time
        
        # Record metrics
        endpoint = request.url.path
        REQUEST_COUNT.labels(method=request.method, endpoint=endpoint, status=response.status_code).inc()
        REQUEST_LATENCY.labels(method=request.method, endpoint=endpoint).observe(process_time)
        
        return response

def track_cost(cost: float, model: str, provider: str):
    """
    Helper function to increment the cost counter.
    Should be called from within the route handler after cost is calculated.
    """
    TOTAL_COST.labels(model=model, provider=provider).inc(cost)
