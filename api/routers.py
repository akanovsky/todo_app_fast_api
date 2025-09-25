# api/routers.py
from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from tasks.models import Task as TaskModel
from django.contrib.auth.models import User
from .schemas import TaskCreate, TaskResponse, TaskUpdate
from .api_key_auth import get_current_user
from asgiref.sync import sync_to_async

router = APIRouter()


@router.post("/tasks/", response_model=TaskResponse)
async def create_task(task: TaskCreate, user: User = Depends(get_current_user)):
    """Vytvoří nový úkol a přiřadí ho k aktuálnímu uživateli."""
    new_task = await sync_to_async(TaskModel.objects.create)(user=user, title=task.title, description=task.description)

    # OPRAVA: Použijeme select_related('user') i zde!
    db_task = await sync_to_async(TaskModel.objects.select_related('user').get)(id=new_task.id)
    return db_task


@router.get("/tasks/", response_model=List[TaskResponse])
async def read_tasks(user: User = Depends(get_current_user)):
    """Vrátí seznam všech úkolů pro aktuálního uživatele."""
    tasks = await sync_to_async(list)(TaskModel.objects.filter(user=user).select_related('user').all())
    return tasks


@router.put("/tasks/{task_id}", response_model=TaskResponse)
async def update_task(task_id: int, task: TaskUpdate, user: User = Depends(get_current_user)):
    """Upraví existující úkol patřící aktuálnímu uživateli."""
    try:
        db_task = await sync_to_async(TaskModel.objects.select_related('user').get)(id=task_id, user=user)
        for key, value in task.dict(exclude_unset=True).items():
            setattr(db_task, key, value)
        await sync_to_async(db_task.save)()
        return db_task
    except TaskModel.DoesNotExist:
        raise HTTPException(status_code=404, detail="Úkol nebyl nalezen nebo k němu nemáte přístup.")


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int, user: User = Depends(get_current_user)):
    """Smaže úkol patřící aktuálnímu uživateli."""
    try:
        db_task = await sync_to_async(TaskModel.objects.get)(id=task_id, user=user)
        await sync_to_async(db_task.delete)()
    except TaskModel.DoesNotExist:
        raise HTTPException(status_code=404, detail="Úkol nebyl nalezen nebo k němu nemáte přístup.")