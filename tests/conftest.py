import os

import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch

os.environ.setdefault("GEMINI_API_KEY", "test-key")
os.environ.setdefault("DATABASE_URL", "postgresql://nexus_user:nexus_password@localhost:5432/nexus")
os.environ.setdefault("REDIS_URL", "redis://localhost:6379/0")

from src.main import app


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def mock_gemini_client():
    with patch("src.main.gemini_client") as mock:
        mock.generate_video = AsyncMock(
            return_value={"job_id": "test_job_123", "status": "processing"}
        )
        mock.check_generation_status = AsyncMock(
            return_value={"job_id": "test_job_123", "status": "generating", "progress": 50}
        )
        mock.retrieve_video = AsyncMock(
            return_value={
                "job_id": "test_job_123",
                "video_url": "s3://nexus/test.mp4",
                "duration": 30,
                "format": "mp4",
            }
        )
        yield mock
