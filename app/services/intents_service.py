import logging

from flask import render_template

from app.config.config import Config
from app.services.intent_processor_service import IntentProcessorService
from app.services.weather.weather_service import WeatherService

# Configure logging
logger = logging.getLogger(__name__)


class IntentsService:
    system_role = None

    @staticmethod
    def initialize_intent_processor_service():
        """
        Initialize the IntentProcessorService singleton instance.
        """
        IntentProcessorService.initialize()

    @staticmethod
    def handle_request(payload):
        query = payload["request"]
        intents_processor = IntentProcessorService()
        intent_response = intents_processor.process_utterance(query)
        return {"type": "statement", "response": intent_response.details.data}

    @staticmethod
    def get_launch_message():
        intents_processor = IntentProcessorService()
        intents_processor.set_random_personality()
        prompt = render_template("launch_prompt")
        response_text = intents_processor.get_ai_response(
            prompt, Config().large_language_model, intents_processor.system_role
        )
        return {"type": "question", "response": response_text}

    @staticmethod
    def get_fallback_message():
        prompt = render_template("fallback_prompt")
        intents_processor = IntentProcessorService()
        response_text = intents_processor.get_ai_response(prompt)
        return {"type": "question", "response": response_text}

    @staticmethod
    def get_goodbye_message():
        prompt = render_template("goodbye_prompt")
        intents_processor = IntentProcessorService()
        response_text = intents_processor.get_ai_response(prompt)
        return {"type": "statement", "response": response_text}

    @staticmethod
    def get_help_message():
        prompt = render_template("help_prompt")
        intents_processor = IntentProcessorService()
        response_text = intents_processor.get_ai_response(prompt)
        return {"type": "question", "response": response_text}

    @staticmethod
    def get_stop_message():
        prompt = render_template("stop_prompt")
        intents_processor = IntentProcessorService()
        response_text = intents_processor.get_ai_response(prompt)
        return {"type": "statement", "response": response_text}

    @staticmethod
    def get_cancel_message():
        prompt = render_template("cancel_prompt")
        intents_processor = IntentProcessorService()
        response_text = intents_processor.get_ai_response(prompt)
        return {"type": "statement", "response": response_text}

    @staticmethod
    def get_session_ended_message():
        prompt = render_template("session_ended_prompt")
        intents_processor = IntentProcessorService()
        response_text = intents_processor.get_ai_response(prompt)
        return {"type": "statement", "response": response_text}

    @staticmethod
    def handle_weather_forecast(payload):
        service = WeatherService()
        slot_info = payload["request"]
        prompt = service.handle_weather_forecast(slot_info)
        intents_processor = IntentProcessorService()
        response_text = intents_processor.get_ai_response(prompt)
        return {"type": "statement", "response": response_text}
