import os
from fastapi import APIRouter, HTTPException, status
from src.schemas.car_schemas import CarAdInput, CarAdOutput
from dotenv import load_dotenv

load_dotenv()
router = APIRouter()

@router.post("/analyze_car_ad", response_model=CarAdOutput)
async def normalize_car_ad(ad: CarAdInput):
    if os.environ.get("LLM_STUB") == "1":
        return CarAdOutput(
            brand="Porsche",
            model="911",
            year=2022,
            engine_type="I6",
            transmission="Automatic",
            confidence=0.95,
            needs_review=False
        )

    raise HTTPException(
        status_code = status.HTTP_501_NOT_IMPLEMENTED,
        detail = "LLM endpoint no implemented yet. Please set LLM_STUB=1 in your environment variables to use the stub response."
    )