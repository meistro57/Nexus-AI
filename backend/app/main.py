from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any

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

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/workflows", response_model=Workflow)
def create_workflow(workflow: Workflow):
    WORKFLOWS[workflow.id] = workflow
    return workflow


@app.get("/workflows", response_model=List[Workflow])
def list_workflows():
    return list(WORKFLOWS.values())


@app.get("/workflows/{workflow_id}", response_model=Workflow)
def get_workflow(workflow_id: str):
    if workflow_id not in WORKFLOWS:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return WORKFLOWS[workflow_id]


def execute_node(node: Node, logs: List[str], context: Dict[str, Any]):
    if node.type == "print":
        message = node.params.get("message", "")
        logs.append(message)
    elif node.type == "add":
        a = node.params.get("a", 0)
        b = node.params.get("b", 0)
        result = a + b
        logs.append(f"{a} + {b} = {result}")
        context[node.id] = result
    else:
        logs.append(f"Unknown node type: {node.type}")


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
