from fastapi import APIRouter, Response
from src.schemas.task_scheme import Task
from src.services.task_service import TaskService

router = APIRouter(prefix = "/tasks", tags=["Tasks"])

@router.get("")
async def get_tasks():
    return {"tasks" : TaskService.get_all_tasks()}

@router.get("/{task_id}")
async def get_by_id(task_id:int):
    task = TaskService.get_task_by_id(task_id)
    return {"task" : task}

@router.post("", status_code = 201)
async def create_task(task: Task):
    return TaskService.create_task(task)

@router.put("/{task_id}")
async def update_task(task_id:int, task:Task):
    return TaskService.update_task(task_id, task)

@router.delete("/{task_id}", status_code = 204)
async def delete_task(task_id:int):
    TaskService.delete_task(task_id)
    return Response(status_code=204)