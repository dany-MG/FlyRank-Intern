from pydantic import BaseModel, Field
from typing import Optional, Literal

class CarAdInput(BaseModel):
    text: str = Field(...,  max_length=1000, description="The text of the car advertisement to be analyzed.")

class CarAdOutput(BaseModel):
    brand: str
    model: str
    year : Optional[int] = None
    engine_type: Literal["I4", "I6", "V6", "V8", "V10", "V12", "EV", "unknown"]
    transmission: Literal["Manual", "Automatic", "CVT", "DCT", "unknown"]
    confidence: float = Field(..., ge = 0.0, le=1.0)
    needs_review: bool
