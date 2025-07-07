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
