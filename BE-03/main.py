from fastapi import FastAPI
from src.database.supabase import supabase

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Server is running and connected to Supabase"}