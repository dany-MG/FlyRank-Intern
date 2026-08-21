from fastapi import FastAPI
from src.routes import meta_routes, report_routes

app = FastAPI(title="PDF Report Generator API", version="1.0.0")
app.include_router(meta_routes.router)
app.include_router(report_routes.router)
