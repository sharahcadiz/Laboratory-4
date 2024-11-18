from fastapi import APIRouter, HTTPException, Depends, Header
from pydantic import BaseModel
from typing import Optional, List
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
API_KEY = os.getenv("LAB4_API_KEY")

router = APIRouter()

class Task(BaseModel):
    task_title: str
    task_desc: str
    is_finished: bool = False

task_db = [
    {"task_id": 1, "task_title": "Laboratory Activity", "task_desc": "Create Lab Act 2", "is_finished": False}
]

def authenticate(api_key: str = Header(None)):
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

@router.get("/tasks", response_model=List[dict], status_code=200)
def get_tasks(api_key: str = Depends(authenticate)):
    if not task_db:
        return {"message": "No tasks available", "status_code": 204}
    return task_db

@router.get("/tasks/{task_id}", status_code=200)
def get_task(task_id: int, api_key: str = Depends(authenticate)):
    task = next((t for t in task_db if t["task_id"] == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.post("/tasks", status_code=201)
def create_task(task: Task, api_key: str = Depends(authenticate)):
    new_task_id = max([t["task_id"] for t in task_db], default=0) + 1
    new_task = {"task_id": new_task_id, **task.dict()}
    task_db.append(new_task)
    return {"message": "Task added", "task": new_task}

@router.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int, api_key: str = Depends(authenticate)):
    for idx, task in enumerate(task_db):
        if task["task_id"] == task_id:
            task_db.pop(idx)
            return
    raise HTTPException(status_code=404, detail="Task not found. Cannot delete.")

@router.patch("/tasks/{task_id}", status_code=204)
def update_task(task_id: int, task: Task, api_key: str = Depends(authenticate)):
    for idx, t in enumerate(task_db):
        if t["task_id"] == task_id:
            task_db[idx].update(task.dict())
            return
    raise HTTPException(status_code=404, detail="Task not found. Cannot update.")
