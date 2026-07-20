from services.llm_service import LLMService
from prompts.planner_prompt import PLANNER_PROMPT
from utils.json_parser import extract_json


class PlannerAgent:

    def __init__(self):
        self.llm = LLMService()

    def create_plan(self, request: str):

        prompt = PLANNER_PROMPT.format(
            request=request
        )

        response = self.llm.generate(prompt)

        try:
            return extract_json(response)

        except Exception as e:
            print("\nPlanner JSON Parse Error:")
            print(e)
            print(response)
            return []