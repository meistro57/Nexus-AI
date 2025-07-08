import sys
from pathlib import Path
from fastapi.testclient import TestClient

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.main import app

client = TestClient(app)

def test_list_agents():
    res = client.get("/agents")
    assert res.status_code == 200
    agents = res.json()
    assert "echo" in agents
    # plugin agent should also be loaded
    assert "uppercase" in agents

def test_test_agent():
    res = client.post("/agents/echo/test", json={"prompt": "hi"})
    assert res.status_code == 200
    assert res.json()["response"] == "ECHO: hi"

    # test plugin agent
    res = client.post("/agents/uppercase/test", json={"prompt": "hi"})
    assert res.status_code == 200
    assert res.json()["response"] == "HI"
