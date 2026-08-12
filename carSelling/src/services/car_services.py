import os
import json
from fastapi import HTTPException, status
from openai import OpenAI
from pydantic import ValidationError
from src.schemas.car_schemas import CarAdInput, CarAdOutput
from src.services.car_logs import _log_quarantine

async def llm_call(ad: CarAdInput):
    client = OpenAI(
        base_url = os.environ["LLM_BASE_URL"],
        api_key = os.environ["LLM_API_KEY"]
    )

    prompt_path = os.path.join("prompts", "normalize_car_ad_v1.md")
    with open(prompt_path, "r", encoding="utf-8") as f:
        system_prompt = f.read()

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
    try:
        res = client.chat.completions.create(
            model = os.environ["LLM_MODEL"],
            temperature = 0.2,
            messages = messages
        )
        raw_output = res.choices[0].message.content
        cleaned_output = raw_output.strip().removeprefix("```json").removesuffix("```").strip()

        return CarAdOutput.model_validate_json(cleaned_output)

    except (json.JSONDecodeError, ValidationError) as e:
        error_details = str(e)
        repair_message = f"Your previous answer was rejected for this reason: {error_details}. Return only corrected JSON matching the schema."

        messages.append({"role" : "assistant", "content" : raw_output})
        messages.append({"role" : "user", "content" : repair_message})

        try:
            res_repair = client.chat.completions.create(
                model = os.environ["LLM_MODEL"],
                temperature = 0.2,
                messages = messages
            )
            raw_output_repair = res_repair.choices[0].message.content
            cleaned_output_repair = raw_output_repair.strip().removeprefix("```json").removesuffix("```").strip()
            return CarAdOutput.model_validate_json(cleaned_output_repair)
        except (json.JSONDecodeError, ValidationError) as e:
            _log_quarantine(ad.text, raw_output_repair, str(e), prompt_ver="v1")
            raise HTTPException(
                status_code = status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail = f"LLM response could not be parsed or validated after repair attempt. Error: {str(e)}"
            )

    except Exception as e:
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = f"An unexpected error occurred while processing the LLM response: {str(e)}"
        )


