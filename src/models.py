import uuid
from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class VideoStyle(str, Enum):
    CINEMATIC = "cinematic"
    DOCUMENTARY = "documentary"
    ARTISTIC = "artistic"
    EDUCATIONAL = "educational"


class VideoFormat(str, Enum):
    MP4 = "mp4"
    WEBM = "webm"
    MOV = "mov"


class VideoGenerationRequest(BaseModel):
    prompt: str = Field(..., min_length=10, max_length=1000)
    duration: int = Field(..., ge=5, le=300)
    style: VideoStyle = VideoStyle.CINEMATIC
    format: VideoFormat = VideoFormat.MP4
    webhook_url: Optional[str] = None
    agent_id: Optional[str] = None
    trace_id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))


class VideoGenerationResponse(BaseModel):
    job_id: str
    status: str
    status_url: str
    message: str


class JobStatusResponse(BaseModel):
    job_id: str
    status: str
    progress: int = 0
    error_message: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class VideoRetrievalResponse(BaseModel):
    job_id: str
    status: str
    video_url: Optional[str] = None
    duration: Optional[int] = None
    format: Optional[str] = None
    created_at: datetime
    completed_at: Optional[datetime] = None
    metadata: dict = {}


class MCPToolDefinition(BaseModel):
    name: str
    description: str
    input_schema: dict
    output_schema: dict


class HealthCheckResponse(BaseModel):
    status: str
    service: str
    uptime_seconds: int
    database_connected: bool
    redis_connected: bool
    gemini_api_ready: bool
