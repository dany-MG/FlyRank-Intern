# W6 - Connect to an AI API
## API Endpoints

### Normalize Car Ad (`POST /normalize-car-ad`)

**Valid Request (Returns 200 OK):**
```bash
curl -X POST http://localhost:8000/normalize-car-ad \\
-H "Content-Type: application/json" \\
-d '{"text": "Selling my bmw m3 2018, 6 in line motor, nothing wrong."}'
```

**Response:**
```json
{
  "brand": "BMW",
  "model": "M3",
  "year": 2018,
  "engine_type": "I6",
  "transmission": "manual",
  "confidence": 0.95,
  "needs_review": false
}
```

**Invalid Request (Returns validation error naming the field):**
```bash
curl -X 'POST' \
'http://localhost:8000/analyze_car_ad' \
-H 'accept:application/json' \
-H 'Content-Type:application/json' \
-d '{"invalid_input":"this test will fail"}' 
```

## Job Card
Input: `{"text": "string, 1-2000 characters"}`
Output: JSON with brand, model, year, engine_type, transmission, confidence, and needs_review.
It must never:
- Invent specifications that are not explicitly mentioned or clearly implied in the text.
- Return free text outside the JSON structure.
- Guess the year or model of the car if they are not mentioned.

## Provider & Setup
Provider: Ollama
Model: gemma3:1b
Environment Variables needed to swap: LLM_BASE_URL, LLM_API_KEY, LLM_MODEL

## Eval Result
Score: 4 out of 8
Date: 2026-08-11
Prompt Version: v1

## Cost
Cost for 1 call: ~650 tokens (0 USD, running locally via Ollama).
Estimate for 10,000 requests/day: $0.00 (Local compute).

## What I'd fix with another day
I would iterate on the prompt to improve the 4/8 evaluation score, specifically refining the instructions for edge cases and implicit car models.

