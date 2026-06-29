from src.models import MCPToolDefinition

GENERATE_VIDEO_TOOL = MCPToolDefinition(
    name="generate_video",
    description="Generate video via Gemini API",
    input_schema={
        "type": "object",
        "properties": {
            "prompt": {"type": "string", "description": "Video description (10-1000 chars)"},
            "duration": {"type": "integer", "description": "Duration in seconds (5-300)"},
            "style": {
                "type": "string",
                "enum": ["cinematic", "documentary", "artistic", "educational"],
            },
            "format": {"type": "string", "enum": ["mp4", "webm", "mov"]},
            "webhook_url": {"type": "string", "description": "Optional callback URL"},
        },
        "required": ["prompt", "duration", "style", "format"],
    },
    output_schema={
        "type": "object",
        "properties": {
            "job_id": {"type": "string"},
            "status": {"type": "string"},
            "status_url": {"type": "string"},
        },
    },
)

CHECK_STATUS_TOOL = MCPToolDefinition(
    name="check_status",
    description="Check video generation job status",
    input_schema={
        "type": "object",
        "properties": {"job_id": {"type": "string"}},
        "required": ["job_id"],
    },
    output_schema={
        "type": "object",
        "properties": {
            "job_id": {"type": "string"},
            "status": {"type": "string"},
            "progress": {"type": "integer"},
        },
    },
)

RETRIEVE_VIDEO_TOOL = MCPToolDefinition(
    name="retrieve_video",
    description="Get completed video URL",
    input_schema={
        "type": "object",
        "properties": {"job_id": {"type": "string"}},
        "required": ["job_id"],
    },
    output_schema={
        "type": "object",
        "properties": {
            "job_id": {"type": "string"},
            "video_url": {"type": "string"},
            "duration": {"type": "integer"},
            "format": {"type": "string"},
        },
    },
)

MCP_TOOLS = [GENERATE_VIDEO_TOOL, CHECK_STATUS_TOOL, RETRIEVE_VIDEO_TOOL]


def get_tool_by_name(name: str) -> MCPToolDefinition:
    for tool in MCP_TOOLS:
        if tool.name == name:
            return tool
    raise ValueError(f"Tool '{name}' not found")
