from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import APIKeyHeader
from fastapi import Depends
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import json
from pathlib import Path
import asyncio
import os

from .nodes import NODE_REGISTRY

from .agents import AGENTS, BaseAgent

API_KEY = os.getenv("NEXUS_API_KEY", "testtoken")
api_key_header = APIKeyHeader(name="Authorization", auto_error=False)


async def get_api_key(api_key: str | None = Depends(api_key_header)):
    if api_key == f"Bearer {API_KEY}":
        return api_key
    raise HTTPException(status_code=401, detail="Unauthorized")

app = FastAPI(title="NEXUS AI Backend")
router = APIRouter(dependencies=[Depends(get_api_key)])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ACTIVE_CONNECTIONS: List[WebSocket] = []


async def broadcast(message: str):
    for ws in list(ACTIVE_CONNECTIONS):
        try:
            await ws.send_text(message)
        except Exception:
            try:
                ACTIVE_CONNECTIONS.remove(ws)
            except ValueError:
                pass


class Node(BaseModel):
    id: str
    type: str
    params: Dict[str, Any] = {}


class Workflow(BaseModel):
    id: str
    name: str
    nodes: List[Node]


class Suggestion(BaseModel):
    message: str
    node_id: Optional[str] = None


WORKFLOWS: Dict[str, Workflow] = {}
DATA_DIR = Path(__file__).resolve().parent / ".." / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# --- Auto-scaling Execution Queue ---
MIN_WORKERS = int(os.getenv("MIN_WORKERS", "1"))
MAX_WORKERS = int(os.getenv("MAX_WORKERS", "5"))
WORKFLOW_QUEUE: asyncio.Queue[str] = asyncio.Queue()
WORKERS: List[asyncio.Task] = []


async def worker():
    while True:
        workflow_id = await WORKFLOW_QUEUE.get()
        try:
            workflow = WORKFLOWS.get(workflow_id)
            if workflow:
                logs: List[str] = []
                context: Dict[str, Any] = {}
                for node in workflow.nodes:
                    await execute_node(node, logs, context)
        finally:
            WORKFLOW_QUEUE.task_done()


async def scale_workers():
    while len(WORKERS) < min(MAX_WORKERS, WORKFLOW_QUEUE.qsize() + MIN_WORKERS):
        task = asyncio.create_task(worker())
        WORKERS.append(task)


@app.on_event("startup")
async def startup_event():
    # start initial workers
    for _ in range(MIN_WORKERS):
        WORKERS.append(asyncio.create_task(worker()))


@app.websocket("/ws/logs")
async def websocket_logs(ws: WebSocket):
    await ws.accept()
    ACTIVE_CONNECTIONS.append(ws)
    try:
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        ACTIVE_CONNECTIONS.remove(ws)


@app.get("/health")
def health_check():
    return {"status": "ok"}


class AgentTest(BaseModel):
    prompt: str


@router.get("/agents")
def list_agents():
    return list(AGENTS.keys())


@router.post("/agents/{agent_name}/test")
async def test_agent(agent_name: str, data: AgentTest):
    agent = AGENTS.get(agent_name)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    response = await agent.run(data.prompt)
    return {"response": response}


@router.post("/workflows", response_model=Workflow)
def create_workflow(workflow: Workflow):
    WORKFLOWS[workflow.id] = workflow
    return workflow


@router.put("/workflows/{workflow_id}", response_model=Workflow)
def update_workflow(workflow_id: str, workflow: Workflow):
    if workflow_id != workflow.id:
        raise HTTPException(status_code=400, detail="ID mismatch")
    if workflow_id not in WORKFLOWS:
        raise HTTPException(status_code=404, detail="Workflow not found")
    WORKFLOWS[workflow_id] = workflow
    return workflow


@router.delete("/workflows/{workflow_id}")
def delete_workflow(workflow_id: str):
    if workflow_id not in WORKFLOWS:
        raise HTTPException(status_code=404, detail="Workflow not found")
    WORKFLOWS.pop(workflow_id)
    path = DATA_DIR / f"{workflow_id}.json"
    if path.exists():
        path.unlink()
    return {"deleted": workflow_id}


@router.post("/workflows/{workflow_id}/save")
def save_workflow(workflow_id: str):
    if workflow_id not in WORKFLOWS:
        raise HTTPException(status_code=404, detail="Workflow not found")
    workflow = WORKFLOWS[workflow_id]
    path = DATA_DIR / f"{workflow_id}.json"
    path.write_text(workflow.json())
    return {"saved": str(path)}


@router.post("/workflows/{workflow_id}/load", response_model=Workflow)
def load_workflow(workflow_id: str):
    path = DATA_DIR / f"{workflow_id}.json"
    if not path.exists():
        raise HTTPException(status_code=404, detail="Workflow file not found")
    data = json.loads(path.read_text())
    workflow = Workflow(**data)
    WORKFLOWS[workflow_id] = workflow
    return workflow


@router.get("/workflows", response_model=List[Workflow])
def list_workflows():
    return list(WORKFLOWS.values())


@router.get("/workflows/{workflow_id}", response_model=Workflow)
def get_workflow(workflow_id: str):
    if workflow_id not in WORKFLOWS:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return WORKFLOWS[workflow_id]


@router.post("/workflows/{workflow_id}/validate")
def validate_workflow_endpoint(workflow_id: str):
    if workflow_id not in WORKFLOWS:
        raise HTTPException(status_code=404, detail="Workflow not found")
    workflow = WORKFLOWS[workflow_id]
    errors: List[str] = []
    for node in workflow.nodes:
        node_cls = NODE_REGISTRY.get(node.type)
        if not node_cls:
            errors.append(f"Unknown node type: {node.type}")
            continue
        errors.extend(node_cls.validate(node.params))
    return {"valid": len(errors) == 0, "errors": errors}


def generate_suggestions(workflow: Workflow) -> List[Suggestion]:
    suggestions: List[Suggestion] = []
    last_print: Optional[str] = None
    for node in workflow.nodes:
        if node.type == "print":
            message = node.params.get("message", "")
            if message == last_print:
                suggestions.append(
                    Suggestion(
                        message="Consecutive print nodes with same message",
                        node_id=node.id,
                    )
                )
            last_print = message
        if node.type == "add":
            a = node.params.get("a", 0)
            b = node.params.get("b", 0)
            if a == 0 or b == 0:
                suggestions.append(
                    Suggestion(message="Adding zero has no effect", node_id=node.id)
                )
    if len(workflow.nodes) > 10:
        suggestions.append(
            Suggestion(message="Large workflow; consider splitting into parts")
        )
    return suggestions


@router.post("/workflows/{workflow_id}/suggest", response_model=List[Suggestion])
def suggest_workflow(workflow_id: str):
    if workflow_id not in WORKFLOWS:
        raise HTTPException(status_code=404, detail="Workflow not found")
    workflow = WORKFLOWS[workflow_id]
    return generate_suggestions(workflow)


async def log(message: str, logs: List[str]):
    logs.append(message)
    await broadcast(message)


async def execute_node(node: Node, logs: List[str], context: Dict[str, Any]):
    node_cls = NODE_REGISTRY.get(node.type)
    if node_cls is not None:
        async def node_log(message: str):
            await log(message, logs)

        await node_cls.execute(node.model_dump(), node_log, context)
    elif node.type == "agent":
        agent_name = node.params.get("agent")
        prompt = node.params.get("prompt", "")
        agent: BaseAgent | None = AGENTS.get(agent_name)
        if agent is None:
            await log(f"Unknown agent: {agent_name}", logs)
        else:
            response = await agent.run(prompt)
            context[node.id] = response
            await log(f"{agent_name} -> {response}", logs)
    else:
        await log(f"Unknown node type: {node.type}", logs)


@router.post("/workflows/{workflow_id}/execute")
async def execute_workflow(workflow_id: str):
    if workflow_id not in WORKFLOWS:
        raise HTTPException(status_code=404, detail="Workflow not found")

    workflow = WORKFLOWS[workflow_id]
    logs: List[str] = []
    context: Dict[str, Any] = {}

    for node in workflow.nodes:
        await execute_node(node, logs, context)

    return {"logs": logs}


@router.post("/workflows/{workflow_id}/enqueue")
async def enqueue_workflow(workflow_id: str):
    if workflow_id not in WORKFLOWS:
        raise HTTPException(status_code=404, detail="Workflow not found")
    await WORKFLOW_QUEUE.put(workflow_id)
    await scale_workers()
    return {"queued": workflow_id, "queue_size": WORKFLOW_QUEUE.qsize()}


@router.get("/queue/status")
def queue_status():
    return {"queue_size": WORKFLOW_QUEUE.qsize(), "workers": len(WORKERS)}

app.include_router(router)
