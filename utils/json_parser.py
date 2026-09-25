import json
import re


def extract_json(text: str):
    """Extracts and parses JSON from raw LLM output even if wrapped in markdown
    or followed by trailing commentary/extra text.
    """
    if not text:
        return None

    # 1. Remove markdown code fences if present
    cleaned = re.sub(r"^```(?:json)?\s*", "", text.strip(), flags=re.MULTILINE)
    cleaned = re.sub(r"```$", "", cleaned.strip(), flags=re.MULTILINE).strip()

    # 2. Try standard json.loads first
    try:
        return json.loads(cleaned)
    except Exception:
        pass

    # 3. Locate the first '{' or '[' and parse using raw_decode
    match = re.search(r"(\{.*\}|)", cleaned, re.DOTALL)
    if match:
        snippet = match.group(0)
    try:
        return json.loads(snippet)
    except Exception:
        pass
    # 4. Handle 'Extra data' by finding the start and decoding the first valid JSON block
    for i, char in enumerate(cleaned):
        if char in ("{", "["):
            try:
                decoder = json.JSONDecoder()
                obj, _ = decoder.raw_decode(cleaned[i:])
                return obj
            except Exception:
                continue

    raise ValueError(f"Could not extract valid JSON from response: {text[:100]}...")