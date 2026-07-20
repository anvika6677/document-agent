import json
import re


def extract_json(text: str):

    # Remove markdown code blocks
    text = re.sub(r"```json", "", text, flags=re.IGNORECASE)
    text = re.sub(r"```", "", text)

    text = text.strip()

    # Extract only JSON object
    start = text.find("{")

    if start != -1:

        end = text.rfind("}")

        if end != -1:
            text = text[start:end + 1]

    return json.loads(text)