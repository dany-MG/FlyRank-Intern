from fastapi import FastAPI
from fastapi.responses import JSONResponse

tasks = [
    {"id": 1, "title" : "Play LMU", "done": False},
    {"id": 2, "title" : "Workout", "done": True},
    {"id": 3, "title" : "Walk the puppies", "done": False}
] 

app = FastAPI()

@app.get("/")
async def root():
    return {"name" : "Task API", "version" : "1.0", "endpoints": ["/tasks"]}

@app.get("/health")
async def health():
    return {"status" : "ok"}

@app.get("/tasks")
async def get_tasks():
    return {"tasks" : tasks}

@app.get("/tasks/{task_id}")
async def get_task(task_id:int):
    for task in tasks:
        if task.get("id") == task_id:
            return {"task" : task}
    return JSONResponse(
        status_code = 404,
        content = {"error" : f"Task {task_id} not found"}
    )

    





