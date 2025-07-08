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
POST /workflows/{id}/validate  # validate workflow structure
POST /workflows/{id}/save      # save workflow to disk
POST /workflows/{id}/load      # load workflow from disk
```

Several node types are implemented:

- `print` – logs a message
- `add` – adds two numbers and logs the result
- `condition` – evaluates a boolean expression using workflow context
- `loop` – logs a message for a configurable number of iterations

Nodes are registered using a simple node factory, allowing new types to be added
by registering additional classes in `app/nodes.py`.

New agent helper endpoints are also available:

- `GET  /agents` – list available agents
- `POST /agents/{name}/test` – run an agent with a prompt for quick testing

Agent plugins can be dropped into `app/plugins` and will be loaded
automatically at startup. An example `uppercase` plugin is included.
