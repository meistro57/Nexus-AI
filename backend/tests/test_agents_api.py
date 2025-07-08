import sys
from pathlib import Path
from fastapi.testclient import TestClient

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.main import app

client = TestClient(app)
HEADERS = {"Authorization": "Bearer testtoken"}

def test_list_agents():
    res = client.get("/agents", headers=HEADERS)
    assert res.status_code == 200
    agents = res.json()
    assert "echo" in agents
    # plugin agent should also be loaded
    assert "uppercase" in agents
    assert "reverse" in agents

def test_test_agent():
    res = client.post("/agents/echo/test", json={"prompt": "hi"}, headers=HEADERS)
    assert res.status_code == 200
    assert res.json()["response"] == "ECHO: hi"

    # test plugin agent
    res = client.post("/agents/uppercase/test", json={"prompt": "hi"}, headers=HEADERS)
    assert res.status_code == 200
    assert res.json()["response"] == "HI"

    # test reverse plugin agent
    res = client.post("/agents/reverse/test", json={"prompt": "abc"}, headers=HEADERS)
    assert res.status_code == 200
    assert res.json()["response"] == "cba"
