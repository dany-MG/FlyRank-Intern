from fastapi import FastAPI
from src.routes.car_routes import router as car_router
from src.routes.meta_routes import router as meta_router
from src.middleware.error_handler import setup_error_handlers

def create_app() -> FastAPI:
    app = FastAPI(title="Car Advertisement Analysis API", version="1.0")
    app.include_router(meta_router)
    app.include_router(car_router)
    setup_error_handlers(app)
    return app

app = create_app()