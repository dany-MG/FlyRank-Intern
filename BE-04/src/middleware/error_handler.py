from fastapi import Request
from fastapi.responses import JSONResponse
from src.errors import TaskNotFoundError, InvalidTaskError

def setup_error_handlers(app):
    @app.exception_handler(TaskNotFoundError)
    async def not_found_handler(request: Request, exc: TaskNotFoundError):
        return JSONResponse(status_code=404, content={"error": exc.message})

    @app.exception_handler(InvalidTaskError)
    async def invalid_task_handler(request: Request, exc: InvalidTaskError):
        return JSONResponse(status_code=400, content={"detail": exc.message})