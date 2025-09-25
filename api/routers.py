# api/routers.py
from fastapi import APIRouter, HTTPException
from typing import List
from tasks.models import Task as TaskModel
from .schemas import Task, TaskCreate

router = APIRouter()

@router.post("/tasks/", response_model=Task)
def create_task(task: TaskCreate):
    # Vytvoří nový úkol
    new_task = TaskModel.objects.create(title=task.title, description=task.description)
    return new_task

@router.get("/tasks/", response_model=List[Task])
def read_tasks():
    # Vrátí seznam všech úkolů
    tasks = TaskModel.objects.all()
    return tasks

@router.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task: TaskCreate):
    # Najde a aktualizuje úkol
    try:
        db_task = TaskModel.objects.get(id=task_id)
        db_task.title = task.title
        db_task.description = task.description
        db_task.save()
        return db_task
    except TaskModel.DoesNotExist:
        raise HTTPException(status_code=404, detail="Task not found")

@router.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    # Najde a smaže úkol
    try:
        db_task = TaskModel.objects.get(id=task_id)
        db_task.delete()
        return {"message": "Task deleted successfully"}
    except TaskModel.DoesNotExist:
        raise HTTPException(status_code=404, detail="Task not found")