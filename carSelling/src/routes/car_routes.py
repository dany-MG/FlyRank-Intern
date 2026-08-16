import os
from fastapi import APIRouter, status
from src.schemas.car_schemas import CarAdInput, CarAdOutput
from src.worker import process_car_ad, celery_app

router = APIRouter()

@router.post("/normalize_car_ad", status_code = status.HTTP_202_ACCEPTED)
async def normalize_car_ad(ad: CarAdInput):
    task = process_car_ad.delay(ad.text)
    return{
        "task_id" : task.id,
        "status" : "processing"
    }

@router.get("/status/{task_id}")
async def get_task_status(task_id : str):
    task_id = celery_app.AsyncResult(task_id)
    if task_id.state == "SUCCESS":
        return {
            "task_id" : str(task_id),
            "status" : "success",
            "result" : task_id.result
        }
    elif task_id.state == "FAILURE":
        return {
            "task_id" : str(task_id),
            "status" : "failure",
            "error" : str(task_id.info)
        }
    else:
        return{
            "task_id" : str(task_id),
            "status" : "pending"
        }
