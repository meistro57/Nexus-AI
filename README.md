# Nexus AI

This repository contains the scaffolding for **NEXUS AI**, a visual workflow designer for orchestrating multi-agent AI systems. The project consists of a frontend that now ships with a rich HTML/JS interface and a FastAPI backend.

## Structure

- `frontend/` – Vite project serving the GUI from `index.html`
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
The development server now serves `index.html`, which contains the interactive workflow builder originally provided in `template.html`.

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

## Docker Deployment

You can run the backend using Docker:

```bash
docker build -t nexus-backend -f backend/Dockerfile backend
docker run -p 8000:8000 nexus-backend
```
