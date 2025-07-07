import json
from fastapi.testclient import TestClient

from app.main import app, WORKFLOWS
from app.nodes import NODE_REGISTRY

client = TestClient(app)


def test_node_registry():
    assert 'print' in NODE_REGISTRY
    assert 'add' in NODE_REGISTRY


def test_workflow_validation_and_execution():
    workflow = {
        "id": "wf1",
        "name": "Demo",
        "nodes": [
            {"id": "1", "type": "print", "params": {"message": "hi"}},
            {"id": "2", "type": "add", "params": {"a": 1, "b": 2}}
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
    assert "1 + 2 = 3" in "\n".join(data["logs"])

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
