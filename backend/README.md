# NEXUS AI Backend

This is a minimal FastAPI server to bootstrap the backend for the NEXUS AI workflow designer.

## Quick Start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API exposes a basic `/health` endpoint and a `/workflows` endpoint for creating workflows.

Additional endpoints allow listing, retrieving and executing workflows:

```
GET  /workflows                # list workflows
GET  /workflows/{id}           # retrieve a workflow
POST /workflows/{id}/execute   # run a workflow and return logs
```

Two simple node types are implemented:

- `print` – logs a message
- `add` – adds two numbers and logs the result
