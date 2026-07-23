import logging
import time
from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI, HTTPException
from prometheus_client import Counter, Histogram

from src.config import get_settings, setup_logging
from src.gemini_client import GeminiClient
from src.models import (
    HealthCheckResponse,
    JobStatusResponse,
    VideoGenerationRequest,
    VideoGenerationResponse,
    VideoRetrievalResponse,
)
from src.tools import MCP_TOOLS

logger = logging.getLogger(__name__)
setup_logging()

video_generations = Counter("nexus_video_generations_total", "Total video generation requests")
generation_duration = Histogram(
    "nexus_video_generation_duration_seconds",
    "Video generation duration",
)
generation_errors = Counter("nexus_video_generation_errors_total", "Total video generation errors")

gemini_client: GeminiClient | None = None
start_time = time.time()


@asynccontextmanager
async def lifespan(app: FastAPI):
    global gemini_client
    gemini_client = GeminiClient()
    logger.info("nexus-gemini-mcp started")
    yield
    logger.info("nexus-gemini-mcp shutdown")


app = FastAPI(title="NEXUS Gemini MCP Server", version="0.1.0", lifespan=lifespan)


@app.post("/tools/generate_video")
async def generate_video(req: VideoGenerationRequest):
    try:
        video_generations.inc()
        with generation_duration.time():
            result = await gemini_client.generate_video(
                prompt=req.prompt,
                duration=req.duration,
                style=req.style.value,
                format=req.format.value,
            )
        return VideoGenerationResponse(
            job_id=result["job_id"],
            status=result["status"],
            status_url=f"/tools/check_status?job_id={result['job_id']}",
            message="Video generation queued",
        )
    except Exception as e:
        generation_errors.inc()
        logger.error("Video generation failed: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.get("/tools/check_status")
async def check_status(job_id: str):
    try:
        result = await gemini_client.check_generation_status(job_id)
        now = datetime.now()
        return JobStatusResponse(
            job_id=result["job_id"],
            status=result["status"],
            progress=result.get("progress", 0),
            created_at=now,
            updated_at=now,
        )
    except Exception as e:
        logger.error("Status check failed: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.get("/tools/retrieve_video")
async def retrieve_video(job_id: str):
    try:
        result = await gemini_client.retrieve_video(job_id)
        now = datetime.now()
        return VideoRetrievalResponse(
            job_id=result["job_id"],
            status="completed",
            video_url=result["video_url"],
            duration=result["duration"],
            format=result["format"],
            created_at=now,
            completed_at=now,
        )
    except Exception as e:
        logger.error("Video retrieval failed: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.get("/health")
async def health_check():
    uptime = int(time.time() - start_time)
    return HealthCheckResponse(
        status="healthy",
        service="nexus-gemini-mcp",
        uptime_seconds=uptime,
        database_connected=True,
        redis_connected=True,
        gemini_api_ready=gemini_client is not None,
    )


@app.get("/mcp/tools")
async def list_mcp_tools():
    return {"tools": [tool.model_dump() for tool in MCP_TOOLS]}


@app.get("/")
async def root():
    return {
        "service": "nexus-gemini-mcp",
        "version": "0.1.0",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "tools": "/mcp/tools",
            "generate": "/tools/generate_video",
            "status": "/tools/check_status",
            "retrieve": "/tools/retrieve_video",
        },
    }


def run() -> None:
    import uvicorn

    settings = get_settings()
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=settings.SERVICE_PORT,
        log_level=settings.LOG_LEVEL.lower(),
    )


if __name__ == "__main__":
    run()
