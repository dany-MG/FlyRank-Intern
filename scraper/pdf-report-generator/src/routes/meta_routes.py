from fastapi import APIRouter

router = APIRouter(tags=["Meta Routes"])

@router.get("/")
def root():
    return {"message": "Welcome to the PDF Report Generator API!"}
    
@router.get("/health")
def health_check():
    return {"status": "ok"}



