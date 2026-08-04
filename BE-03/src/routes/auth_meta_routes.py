from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def root():
    return {"message": "Server is running and connected to Supabase"}