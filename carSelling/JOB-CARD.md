# Job Card
**What it does?:** Normalize used car selling announcement's description and extracts its specifications into a structured format.
**Input:**
{"text" : "string, 1-2000 characters"}

**Output:**
{
  "brand": "string (canonical name, e.g., BMW, Volkswagen)",
  "model": "string",
  "year": "number (YYYY) or null",
  "engine_type": "one of [I4 | I6 | V6 | V8 | V10 | V12 | EV | unknown]",
  "transmission": "one of [manual | automatic | dct | cvt | unknown]",
  "confidence": "0.0-1.0",
  "needs_review": "boolean"
}

**It must never:**
* Invent specifications that are not explicitly mentioned or clearly implied in the text.
* Return free text outside the JSON structure.
* Guess the year or model of the car if they are not mentioned.

**When unsure it should:**
* Use an "uknown" value to closed lists (enums), assign a confidence value lower than 0.5 and mark "needs_review" as true.
