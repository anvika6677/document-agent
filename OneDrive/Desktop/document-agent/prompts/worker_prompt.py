WORKER_PROMPT = """
You are an expert technical writer.

Topic:
{topic}

Sections:
{sections}

Generate detailed content for every section.

Rules:
- Return ONLY valid JSON.
- Use the EXACT section names provided as the JSON keys.
- Do NOT rename any section.
- Every section must appear exactly once.
- Each section should contain at least 150 words.
- Do not include markdown.
- Do not include explanations.
"""