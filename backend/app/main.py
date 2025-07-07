from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import json
from pathlib import Path

from .nodes import NODE_REGISTRY

app = FastAPI(title="NEXUS AI Backend")

class Node(BaseModel):
    id: str
    type: str
    params: Dict[str, Any] = {}


class Workflow(BaseModel):
    id: str
    name: str
    nodes: List[Node]


WORKFLOWS: Dict[str, Workflow] = {}
DATA_DIR = Path(__file__).resolve().parent / ".." / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/workflows", response_model=Workflow)
def create_workflow(workflow: Workflow):
    WORKFLOWS[workflow.id] = workflow
    return workflow

@app.post("/workflows/{workflow_id}/save")
def save_workflow(workflow_id: str):
    if workflow_id not in WORKFLOWS:
        raise HTTPException(status_code=404, detail="Workflow not found")
    workflow = WORKFLOWS[workflow_id]
    path = DATA_DIR / f"{workflow_id}.json"
    path.write_text(workflow.json())
    return {"saved": str(path)}

@app.post("/workflows/{workflow_id}/load", response_model=Workflow)
def load_workflow(workflow_id: str):
    path = DATA_DIR / f"{workflow_id}.json"
    if not path.exists():
        raise HTTPException(status_code=404, detail="Workflow file not found")
    data = json.loads(path.read_text())
    workflow = Workflow(**data)
    WORKFLOWS[workflow_id] = workflow
    return workflow


@app.get("/workflows", response_model=List[Workflow])
def list_workflows():
    return list(WORKFLOWS.values())


@app.get("/workflows/{workflow_id}", response_model=Workflow)
def get_workflow(workflow_id: str):
    if workflow_id not in WORKFLOWS:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return WORKFLOWS[workflow_id]

@app.post("/workflows/{workflow_id}/validate")
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


def execute_node(node: Node, logs: List[str], context: Dict[str, Any]):
    node_cls = NODE_REGISTRY.get(node.type)
    if not node_cls:
        logs.append(f"Unknown node type: {node.type}")
        return
    node_cls.execute(node.dict(), logs, context)


@app.post("/workflows/{workflow_id}/execute")
def execute_workflow(workflow_id: str):
    if workflow_id not in WORKFLOWS:
        raise HTTPException(status_code=404, detail="Workflow not found")

    workflow = WORKFLOWS[workflow_id]
    logs: List[str] = []
    context: Dict[str, Any] = {}

    for node in workflow.nodes:
        execute_node(node, logs, context)

    return {"logs": logs}
