from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

class Task(BaseModel):
    task_title: str
    task_desc: str
    is_finished: bool = False

task_db = [
    {"task_id": 1, "task_title": "Laboratory Activity", "task_desc": "Create Lab Act 2", "is_finished": False}
]

@router.get("/tasks/{task_id}")
def get_task(task_id: Optional[int] = None):
    if task_id:
        for task in task_db:
            if task["task_id"] == task_id:
                return {"status": "ok", "result": task}
        raise HTTPException(status_code=404, detail={"error": "Task not found"})
    return {"status": "ok", "result": task_db}

@router.post("/tasks")
def create_task(task: Task):
    new_task_id = max([t["task_id"] for t in task_db], default=0) + 1
    new_task = {"task_id": new_task_id, **task.dict()}
    task_db.append(new_task)
    return {"status": "ok", "task": new_task}

@router.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for idx, task in enumerate(task_db):
        if task["task_id"] == task_id:
            removed_task = task_db.pop(idx)
            return {"status": "ok", "removed_data": removed_task}
    raise HTTPException(status_code=404, detail={"error": "Task not found. Record cannot be deleted"})

@router.patch("/tasks/{task_id}")
def update_task(task_id: int, task: Task):
    for idx, t in enumerate(task_db):
        if t["task_id"] == task_id:
            task_db[idx]["task_title"] = task.task_title
            task_db[idx]["task_desc"] = task.task_desc
            task_db[idx]["is_finished"] = task.is_finished
            return {"status": "ok", "updated_data": task_db[idx]}
    raise HTTPException(status_code=404, detail={"error": "Task not found. Record cannot be updated"})
