from services.llm_service import LLMService
from prompts.worker_prompt import WORKER_PROMPT
from utils.json_parser import extract_json


class WorkerAgent:

    def __init__(self):
        self.llm = LLMService()

    def generate_sections(self, topic: str, sections: list):

        prompt = WORKER_PROMPT.format(
            topic=topic,
            sections=", ".join(sections)
        )

        response = self.llm.generate(prompt)

        print("\n===== Worker Response =====")
        print(response)

        try:
            return extract_json(response)

        except Exception as e:
            print("\nWorker JSON Parse Error:")
            print(e)
            print(response)
            return {}