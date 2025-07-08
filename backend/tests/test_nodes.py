import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient
from app.main import app, WORKFLOWS
from app.nodes import NODE_REGISTRY

client = TestClient(app)
HEADERS = {"Authorization": "Bearer testtoken"}


def test_node_registry():
    assert 'print' in NODE_REGISTRY
    assert 'add' in NODE_REGISTRY
    assert 'condition' in NODE_REGISTRY
    assert 'loop' in NODE_REGISTRY
    assert 'multiply' in NODE_REGISTRY
    assert 'subtract' in NODE_REGISTRY
    assert 'divide' in NODE_REGISTRY
    assert 'power' in NODE_REGISTRY
    assert 'modulo' in NODE_REGISTRY


def test_workflow_validation_and_execution():
    workflow = {
        "id": "wf1",
        "name": "Demo",
        "nodes": [
            {"id": "1", "type": "print", "params": {"message": "hi"}},
            {"id": "2", "type": "add", "params": {"a": 1, "b": 2}},
            {"id": "3", "type": "multiply", "params": {"a": 3, "b": 4}},
            {"id": "4", "type": "subtract", "params": {"a": 5, "b": 3}},
            {"id": "5", "type": "divide", "params": {"a": 8, "b": 2}},
            {"id": "6", "type": "power", "params": {"a": 2, "b": 3}},
            {"id": "7", "type": "modulo", "params": {"a": 7, "b": 4}},
            {"id": "8", "type": "condition", "params": {"expression": "1 < 2"}},
            {"id": "9", "type": "loop", "params": {"count": 2}},
            {"id": "10", "type": "delay", "params": {"ms": 10}}
        ]
    }
    res = client.post("/workflows", json=workflow, headers=HEADERS)
    assert res.status_code == 200
    # validate
    res = client.post("/workflows/wf1/validate", headers=HEADERS)
    data = res.json()
    assert data["valid"]

    # execute
    res = client.post("/workflows/wf1/execute", headers=HEADERS)
    data = res.json()
    log_text = "\n".join(data["logs"])
    assert "1 + 2 = 3" in log_text
    assert "3 * 4 = 12" in log_text
    assert "5 - 3 = 2" in log_text
    assert "8 / 2 = 4.0" in log_text
    assert "2 ** 3 = 8" in log_text
    assert "7 % 4 = 3" in log_text
    assert "1 < 2 -> True" in log_text
    assert "loop 1/2" in log_text

    # save
    res = client.post("/workflows/wf1/save", headers=HEADERS)
    assert res.status_code == 200
    saved = json.loads(res.content.decode())
    path = saved["saved"]
    assert path

    # delete memory and load
    WORKFLOWS.pop("wf1")
    assert "wf1" not in WORKFLOWS
    res = client.post("/workflows/wf1/load", headers=HEADERS)
    assert res.status_code == 200
    assert "wf1" in WORKFLOWS
