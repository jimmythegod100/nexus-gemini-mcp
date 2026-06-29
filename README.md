# NEXUS Gemini MCP Server

MCP server for Google Gemini video generation API.

## What This Is

An async FastAPI service that exposes Gemini video generation as MCP tools for Cursor agents.

## Quick Start

```bash
poetry install
poetry run nexus-gemini-mcp
```

Service runs on http://localhost:8001

## MCP Tools

### generate_video
Input: {prompt, duration, style, format, webhook_url}
Output: {job_id, status, status_url}

### check_status
Input: {job_id}
Output: {job_id, status, progress}

### retrieve_video
Input: {job_id}
Output: {job_id, status, video_url, duration, format}

## Endpoints

- GET /health - Health check
- GET /mcp/tools - MCP tool discovery
- POST /tools/generate_video - Generate video
- GET /tools/check_status - Poll status
- GET /tools/retrieve_video - Get result

## Testing

```bash
poetry run pytest --cov=src
```

## Docker

```bash
docker build -t nexus-gemini-mcp .
docker run -p 8001:8001 -e GEMINI_API_KEY=... nexus-gemini-mcp
```
