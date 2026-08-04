from fastapi import FastAPI
from src.routes import auth_meta_routes, auth_routes

def create_app() -> FastAPI:
    app = FastAPI(title = "BE-03", version="1.0")
    app.include_router(auth_meta_routes.router)
    app.include_router(auth_routes.router)

    return app

app = create_app()