from fastapi import FastAPI
from src.routes.meta_routes import router as meta_router
from src.routes.task_routes import router as tasks_router
from src.middleware.error_handler import setup_error_handlers

def create_app() -> FastAPI:
    app = FastAPI(title= "BE-01", version = "1.0")
    app.include_router(meta_router)
    app.include_router(tasks_router)

    setup_error_handlers(app)

    return app

app = create_app()

