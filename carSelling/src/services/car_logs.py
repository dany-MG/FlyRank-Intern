import os
import json

def _log_quarantine(input_text, raw_output, error_msg, prompt_ver="v1"):
    os.makedirs("logs", exist_ok=True)
    log_entry = {
        "input": input_text,
        "raw_output": raw_output,
        "error": error_msg,
        "prompt_version": prompt_ver
    }

    with open(os.path.join("logs", "quarantine.jsonl"), "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry) + "\n")