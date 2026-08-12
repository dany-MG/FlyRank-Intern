from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def root():
    """Root endpoint that returns basic information about the API."""
    return {"name" : "Car Advertisement Analysis API", "version" : "1.0", "endpoints": ["/analyze_car_ad", "/health"]}

@router.get("/health")
async def health_check():
    """Health check endpoint that returns the status of the API."""
    return {"status" : "ok"}