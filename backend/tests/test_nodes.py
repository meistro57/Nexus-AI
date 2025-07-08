import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient
from app.main import app, WORKFLOWS
from app.nodes import NODE_REGISTRY

client = TestClient(app)


def test_node_registry():
    assert 'print' in NODE_REGISTRY
    assert 'add' in NODE_REGISTRY
    assert 'condition' in NODE_REGISTRY
    assert 'loop' in NODE_REGISTRY


def test_workflow_validation_and_execution():
    workflow = {
        "id": "wf1",
        "name": "Demo",
        "nodes": [
            {"id": "1", "type": "print", "params": {"message": "hi"}},
            {"id": "2", "type": "add", "params": {"a": 1, "b": 2}},
            {"id": "3", "type": "condition", "params": {"expression": "1 < 2"}},
            {"id": "4", "type": "loop", "params": {"count": 2}}
        ]
    }
    res = client.post("/workflows", json=workflow)
    assert res.status_code == 200
    # validate
    res = client.post("/workflows/wf1/validate")
    data = res.json()
    assert data["valid"]

    # execute
    res = client.post("/workflows/wf1/execute")
    data = res.json()
    log_text = "\n".join(data["logs"])
    assert "1 + 2 = 3" in log_text
    assert "1 < 2 -> True" in log_text
    assert "loop 1/2" in log_text

    # save
    res = client.post("/workflows/wf1/save")
    assert res.status_code == 200
    saved = json.loads(res.content.decode())
    path = saved["saved"]
    assert path

    # delete memory and load
    WORKFLOWS.pop("wf1")
    assert "wf1" not in WORKFLOWS
    res = client.post("/workflows/wf1/load")
    assert res.status_code == 200
    assert "wf1" in WORKFLOWS
