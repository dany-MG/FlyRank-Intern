from pydantic import BaseModel
from typing import Optional

class Book(BaseModel):
    title : str
    product_url : str
    price_text:str
    price_gbp : float
    availability_text : str
    rating_text: Optional[str]
    description_text : Optional[str]
    source_page: str
    fetched_at : str

     
