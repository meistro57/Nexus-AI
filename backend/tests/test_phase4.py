import sys
import time
from pathlib import Path
from fastapi.testclient import TestClient

sys.path.append(str(Path(__file__).resolve().parents[1]))
from app.main import app, WORKFLOW_QUEUE

client = TestClient(app)

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
    res = client.post("/workflows", json=wf)
    assert res.status_code == 200
    res = client.post("/workflows/wf_p4/suggest")
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
    client.post("/workflows", json=wf)
    res = client.post("/workflows/wf_p4q/enqueue")
    assert res.status_code == 200
    # allow worker to process
    time.sleep(0.1)
    status = client.get("/queue/status").json()
    assert status["queue_size"] == 0
