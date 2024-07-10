# app/services/ai/__init__.py
from .ai_service import AIService
from .ai_service_instance import AIServiceSingleton

__all__ = ["AIService", "AIServiceSingleton"]
