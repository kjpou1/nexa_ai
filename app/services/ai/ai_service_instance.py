from app.models.singleton import SingletonMeta
from app.services.ai.ai_service import AIService


class AIServiceSingleton(metaclass=SingletonMeta):
    _initialized = False

    def __init__(self, config_path="config/model_configs.json"):
        if not AIServiceSingleton._initialized:
            self.instance = AIService(config_path)
            AIServiceSingleton._initialized = True

    @classmethod
    def get_instance(cls):
        return cls().instance
