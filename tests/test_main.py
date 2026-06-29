def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_mcp_tools_list(client):
    response = client.get("/mcp/tools")
    assert response.status_code == 200
    tools = response.json()["tools"]
    assert len(tools) >= 3
    tool_names = [t["name"] for t in tools]
    assert "generate_video" in tool_names
    assert "check_status" in tool_names
    assert "retrieve_video" in tool_names


def test_generate_video(client, mock_gemini_client):
    payload = {
        "prompt": "A beautiful sunset over mountains",
        "duration": 30,
        "style": "cinematic",
        "format": "mp4",
    }
    response = client.post("/tools/generate_video", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "job_id" in data


def test_invalid_video_request(client):
    payload = {"prompt": "short", "duration": 1, "style": "cinematic", "format": "mp4"}
    response = client.post("/tools/generate_video", json=payload)
    assert response.status_code == 422
