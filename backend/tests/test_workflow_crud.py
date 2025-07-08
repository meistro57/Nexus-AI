import sys
from pathlib import Path
from fastapi.testclient import TestClient

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.main import app, WORKFLOWS

client = TestClient(app)
HEADERS = {"Authorization": "Bearer testtoken"}


def test_update_and_delete_workflow():
    workflow = {
        "id": "crud1",
        "name": "CRUD",
        "nodes": [{"id": "1", "type": "print", "params": {"message": "hello"}}],
    }
    res = client.post("/workflows", json=workflow, headers=HEADERS)
    assert res.status_code == 200

    updated = workflow.copy()
    updated["name"] = "Updated"
    res = client.put(f"/workflows/{workflow['id']}", json=updated, headers=HEADERS)
    assert res.status_code == 200
    assert res.json()["name"] == "Updated"

    res = client.delete(f"/workflows/{workflow['id']}", headers=HEADERS)
    assert res.status_code == 200
    assert workflow["id"] not in WORKFLOWS
