FREE_MODELS = [
    "poolside/laguna-xs.2:free",
    "cohere/north-mini-code:free"
]


class ModelManager:

    def __init__(self):
        self.models = FREE_MODELS

    def get_models(self):
        return self.models