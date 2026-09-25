from services.llm_service import LLMService
from prompts.planner_prompt import PLANNER_PROMPT
from utils.json_parser import extract_json


class PlannerAgent:

    def __init__(self):
        self.llm = LLMService()

    def create_plan(self, request: str) -> list[dict]:
        prompt = PLANNER_PROMPT.format(request=request)
        response = self.llm.generate(prompt)

        try:
            plan = extract_json(response)
            if isinstance(plan, list):
                return plan
            return []
        except Exception as e:
            print(f"[PlannerAgent Error]: {e}")
            return []