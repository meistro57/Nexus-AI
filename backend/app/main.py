from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI(title="NEXUS AI Backend")

class Workflow(BaseModel):
    id: str
    name: str
    nodes: List[dict]

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/workflows", response_model=Workflow)
def create_workflow(workflow: Workflow):
    return workflow
