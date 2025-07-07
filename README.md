# Nexus AI

This repository contains the initial scaffolding for **NEXUS AI**, a visual workflow designer for orchestrating multi-agent AI systems. The project consists of a React-based frontend and a FastAPI backend.

## Structure

- `frontend/` – Vite + React application for the user interface
- `backend/` – FastAPI server providing REST and WebSocket APIs
- `Project_Overview.md` – High-level project specification
- `roadmap.md` – Timeline of planned features and phases

## Getting Started

You can quickly update the repository and launch both the backend and
frontend servers with the provided `start.sh` script:

```bash
./start.sh
```

To run the servers manually follow the steps below.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Both servers will start locally and allow you to connect the frontend to the backend as development progresses.

### Phase 2 Progress

The backend now includes a simple node factory and workflow validation logic. Workflows can also be saved to and loaded from disk using the new `/save` and `/load` endpoints.

## Development Roadmap

See [roadmap.md](roadmap.md) for upcoming milestones and future plans.
