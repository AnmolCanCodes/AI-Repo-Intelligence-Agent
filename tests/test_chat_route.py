import sys
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


@patch("app.graph.nodes.create_llm")
def test_chat_returns_503_when_llm_not_configured(mock_create_llm):
    mock_create_llm.side_effect = ValueError("HF_TOKEN is not set in environment variables or .env file.")

    response = client.post("/api/v1/chat", json={"question": "What does this repo do?"})

    assert response.status_code == 503
    assert "HF_TOKEN" in response.json()["detail"]
