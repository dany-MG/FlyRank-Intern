import os
import json
from fastapi import HTTPException, status
from openai import OpenAI
from src.schemas.car_schemas import CarAdInput

async def llm_call(ad: CarAdInput):
    client = OpenAI(
        base_url = os.environ["LLM_BASE_URL"],
        api_key = os.environ["LLM_API_KEY"]
    )

    prompt_path = os.path.join("prompts", "normalize_car_ad_v1.md")
    with open(prompt_path, "r", encoding="utf-8") as f:
        system_prompt = f.read()

    try:
        res = client.chat.completions.create(
            model = os.environ["LLM_MODEL"],
            temperature = 0.1,
            messages = [
                {
                    "role" : "system",
                    "content" : system_prompt
                },

                 {
                     "role" : "user",
                     "content" : json.dumps({"text" : ad.text})
                 }
            ]
        )
        raw_output = res.choices[0].message.content

        return {"raw_model_response" : raw_output}

    except Exception as e:
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = f"Error calling LLM: {str(e)}"
        )


