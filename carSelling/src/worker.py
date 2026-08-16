from celery import Celery
import asyncio
from dotenv import load_dotenv
from src.schemas.car_schemas import CarAdInput, CarAdOutput
from src.services.car_services import llm_call

load_dotenv()

celery_app = Celery(
    "car_app",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

@celery_app.task(bind=True, max_retries=3, default_retry_delay=5)
def process_car_ad(self, text:str):
    try:
        ad_input = CarAdInput(text=text)
        pydantic_out = asyncio.run(llm_call(ad_input))
        return pydantic_out.model_dump()
    except Exception as e:
        raise self.retry(exc=e)

        