import os
import json
import time
from fastapi import HTTPException, status
from openai import OpenAI, APITimeoutError, APIStatusError
from pydantic import ValidationError
from src.schemas.car_schemas import CarAdInput, CarAdOutput
from src.services.car_logs import _log_quarantine, _log_cost

async def llm_call(ad: CarAdInput) -> CarAdOutput:

    if os.environ.get("LLM_ENABLED", "true").lower() == "false":
        return CarAdOutput(
            brand="unknown", 
            model="unknown", 
            year=None,
            engine_type="unknown", 
            transmission="unknown",
            confidence=0.0, 
            needs_review=True
        )
    
    client = OpenAI(
        base_url = os.environ["LLM_BASE_URL"],
        api_key = os.environ["LLM_API_KEY"],
        timeout = 30,
        max_retries = 2
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

    start_time = time.time()
    repairs = 0
    input_tokens = 0
    output_tokens = 0
    try:
        res = client.chat.completions.create(
            model = os.environ["LLM_MODEL"],
            temperature = 0.2,
            messages = messages
        )

        if res.usage:
            input_tokens += res.usage.prompt_tokens
            output_tokens += res.usage.completion_tokens

        raw_output = res.choices[0].message.content
        cleaned_output = raw_output.strip().removeprefix("```json").removesuffix("```").strip()

        duration_ms = int((time.time() - start_time) * 1000)
        _log_cost("v1", os.environ["LLM_MODEL"],input_tokens, output_tokens, duration_ms, repairs)

        return CarAdOutput.model_validate_json(cleaned_output)

    except (json.JSONDecodeError, ValidationError) as e:
        repairs += 1
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

            if res_repair.usage:
                input_tokens += res_repair.usage.prompt_tokens
                output_tokens += res_repair.usage.completion_tokens

            raw_output_repair = res_repair.choices[0].message.content
            cleaned_output_repair = raw_output_repair.strip().removeprefix("```json").removesuffix("```").strip()

            duration_ms = int((time.time() - start_time) * 1000)
            _log_cost("v1", os.environ["LLM_MODEL"],input_tokens, output_tokens, duration_ms, repairs)
            return CarAdOutput.model_validate_json(cleaned_output_repair)
        except (json.JSONDecodeError, ValidationError) as e:
            duration_ms = int((time.time() - start_time) * 1000)
            _log_cost("v1", os.environ["LLM_MODEL"],input_tokens, output_tokens, duration_ms, repairs)
            _log_quarantine(ad.text, raw_output_repair, str(e), prompt_ver="v1")
            raise HTTPException(
                status_code = status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail = f"LLM response could not be parsed or validated after repair attempt. Error: {str(e)}"
            )

    except APITimeoutError as e:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="AI service timeout."
        )

    except APIStatusError as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=f"AI provider error: {e.message}"
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}"
        )



