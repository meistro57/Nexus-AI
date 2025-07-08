import sys
import time
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
HEADERS = {"Authorization": "Bearer testtoken"}


def test_suggestions_endpoint():
    wf = {
        "id": "wf_p4",
        "name": "Phase4",
        "nodes": [
            {"id": "1", "type": "print", "params": {"message": "dup"}},
            {"id": "2", "type": "print", "params": {"message": "dup"}},
            {"id": "3", "type": "add", "params": {"a": 0, "b": 5}}
        ]
    }
    res = client.post("/workflows", json=wf, headers=HEADERS)
    assert res.status_code == 200
    res = client.post("/workflows/wf_p4/suggest", headers=HEADERS)
    assert res.status_code == 200
    data = res.json()
    assert any("Consecutive print" in s["message"] for s in data)
    assert any("Adding zero" in s["message"] for s in data)


def test_enqueue_and_queue_status():
    wf = {
        "id": "wf_p4q",
        "name": "EnqueueTest",
        "nodes": [
            {"id": "1", "type": "print", "params": {"message": "hi"}}
        ]
    }
    client.post("/workflows", json=wf, headers=HEADERS)
    res = client.post("/workflows/wf_p4q/enqueue", headers=HEADERS)
    assert res.status_code == 200
    # allow worker to process
    time.sleep(0.1)
    status = client.get("/queue/status", headers=HEADERS).json()
    assert status["queue_size"] == 0
