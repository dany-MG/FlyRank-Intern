from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel

tasks = [
    {"id": 1, "title" : "Play LMU", "done": False},
    {"id": 2, "title" : "Workout", "done": True},
    {"id": 3, "title" : "Walk the puppies", "done": False}
] 

class Task(BaseModel):
    id: int  | None = None
    title: str | None = None
    done : bool = False

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

@app.post("/tasks", status_code=201)
async def create_task(task: Task):
    if task.title is None or task.title.strip() == "":
        raise HTTPException(
            status_code = 400,
            detail = "Task title is required"
        )
    t_id = len(tasks) + 1
    task.done = False
    new_task = {"id": t_id, "title": task.title, "done": task.done}
    tasks.append(new_task)
    return new_task

@app.put("/tasks/{id}")
async def update_task(id:int, task:Task):
    if task.title is not None and task.title.strip() == "":
        raise HTTPException(
            status_code = 400,
            detail = "Task title is required"
        )
    
    for t in tasks:
        if t.get("id") == id:
            if task.title is not None:
                t["title"] = task.title
            if task.done is not None:
                t["done"] = task.done
            return task
    
    raise HTTPException(
        status_code = 404,
        detail = f"Task {id} not found"
    )
            
@app.delete("/tasks/{id}")
async def delete_taks(id:int):
    for task in tasks:
        if task.get("id") == id:
            tasks.remove(task)
            return Response(status_code=204)
        
    raise HTTPException(
        status_code = 404,
        detail = f"Task {id} not found"
    )
        
    
        



    




