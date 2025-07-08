import sys
from pathlib import Path
from fastapi.testclient import TestClient

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.main import app

client = TestClient(app)
HEADERS = {"Authorization": "Bearer testtoken"}


def test_execute_agent_node():
    workflow = {
        "id": "w1",
        "name": "Agent Workflow",
        "nodes": [
            {
                "id": "1",
                "type": "agent",
                "params": {"agent": "echo", "prompt": "hello"},
            }
        ]
    }
    res = client.post("/workflows", json=workflow, headers=HEADERS)
    assert res.status_code == 200

    with client.websocket_connect("/ws/logs") as ws:
        exec_res = client.post(f"/workflows/{workflow['id']}/execute", headers=HEADERS)
        assert exec_res.status_code == 200
        data = exec_res.json()
        assert "ECHO: hello" in data["logs"][-1]
        # Receive the same log over websocket
        msg = ws.receive_text()
        assert "ECHO: hello" in msg
