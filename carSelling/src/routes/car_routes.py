import os
from fastapi import APIRouter
from src.schemas.car_schemas import CarAdInput, CarAdOutput
from src.services.car_services import llm_call

router = APIRouter()

@router.post("/normalize_car_ad")
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
    llm_response = await llm_call(ad)
    return llm_response