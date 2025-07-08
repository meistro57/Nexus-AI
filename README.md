# Nexus AI

This repository contains the scaffolding for **NEXUS AI**, a visual workflow designer for orchestrating multi-agent AI systems. It includes a React-based frontend built with Next.js and a FastAPI backend.

## Structure

- `frontend/` – Next.js project that now embeds the Node-RED editor
- `backend/` – FastAPI server providing REST and WebSocket APIs
- `AGENTS.md` – Internal project notes and suggestions
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

# Start a local Node-RED instance separately
npm install -g node-red
node-red
```
The development server hosts a simple Next.js wrapper that displays the
Node-RED editor in an iframe.

Set `NEXT_PUBLIC_NODE_RED_URL` to change the embedded editor URL.

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

The backend now includes a simple node factory and workflow validation logic. Workflows can be saved to and loaded from disk using the `/save` and `/load` endpoints. Additional update and delete endpoints were added along with a new `multiply` node. The frontend has been rewritten with ReactFlow for improved node editing.

## Development Roadmap

See [roadmap.md](roadmap.md) for upcoming milestones and future plans.

## Docker Deployment

You can run the backend using Docker:

```bash
docker build -t nexus-backend -f backend/Dockerfile backend
docker run -p 8000:8000 nexus-backend
```
![image](https://github.com/user-attachments/assets/5be6e6a4-3695-47f6-bcc2-aa32fc6779db)
