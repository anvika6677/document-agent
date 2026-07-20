from openai import OpenAI
from openai import RateLimitError, APIError, APIConnectionError

from core.config import OPENROUTER_API_KEY
from services.model_manager import ModelManager


class LLMService:

    def __init__(self):

        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=OPENROUTER_API_KEY,
        )

        self.model_manager = ModelManager()

    def generate(self, prompt: str):

        models = self.model_manager.get_models()

        last_exception = None

        for model in models:

            try:

                print(f"\nTrying model: {model}")
                print("\n===== Calling LLM =====")

                response = self.client.chat.completions.create(
                    model=model,
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0
                )

                print(f"✅ Using model: {model}")

                return response.choices[0].message.content

            except (RateLimitError, APIError, APIConnectionError) as e:

                print(f"❌ {model} failed.")
                print(f"Reason: {e}")

                last_exception = e

                continue

        raise Exception(
            "No available model could generate a response."
        ) from last_exception