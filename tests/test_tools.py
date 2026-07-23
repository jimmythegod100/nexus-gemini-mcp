from src.tools import MCP_TOOLS, get_tool_by_name


def test_mcp_tools_count():
    assert len(MCP_TOOLS) == 3


def test_get_tool_by_name():
    tool = get_tool_by_name("generate_video")
    assert tool.name == "generate_video"
    assert "prompt" in tool.input_schema["properties"]


def test_get_tool_by_name_invalid():
    try:
        get_tool_by_name("nonexistent")
        raise AssertionError("Expected ValueError")
    except ValueError as e:
        assert "nonexistent" in str(e)
