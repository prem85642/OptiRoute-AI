from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response, FileResponse
from src.api.endpoints import router

from src.api.middleware import MetricsMiddleware

# Load environment variables
load_dotenv()

app = FastAPI(title="OptiRoute AI: Cost-Aware LLM Scaling API")

# Add Middleware
app.add_middleware(MetricsMiddleware)

# Include Routes
app.include_router(router)

# Mount Frontend Static Assets
app.mount("/static", StaticFiles(directory="src/frontend"), name="static")

@app.get("/")
async def read_index():
    return FileResponse("src/frontend/index.html")



@app.get("/metrics")
async def metrics():
    """
    Endpoint for Prometheus to scrape.
    """
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.api.main:app", host="0.0.0.0", port=8000, reload=True)
