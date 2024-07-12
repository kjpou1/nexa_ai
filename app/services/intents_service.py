import logging
import random

from flask import render_template

from app.services.ai.ai_service_instance import AIServiceSingleton
from app.services.weather.weather_service import WeatherService

# Configure logging
logger = logging.getLogger(__name__)


class IntentsService:
    # model_identifier = "gpt-4o"  # "llama3"
    model_identifier = "llama3"
    # model_identifier = "gpt-3.5"
    system_role = None

    @staticmethod
    def set_personality(personality: str):
        """
        Sets the personality of the assistant for the system role.

        Args:
            personality (str): The personality description for the assistant.
        """
        IntentsService.system_role = personality
        logger.info("System role set to: %s", personality)

    @staticmethod
    def set_random_personality():
        """
        Sets a random personality for the assistant.
        """
        personalities = [
            # Professional and friendly personalities
            "You are a helpful and friendly assistant.",
            "You are a witty and humorous assistant.",
            "You are a calm and professional assistant.",
            "You are a knowledgeable and detail-oriented assistant.",
            "You are a cheerful and enthusiastic assistant.",
            "You are a serious and efficient assistant.",
            "You are a snarky but helpful assistant.",
            "You are a compassionate and empathetic assistant.",
            "You are a playful and creative assistant.",
            "You are a wise and sage-like assistant.",
            "You are a bold and adventurous assistant.",
            "You are a meticulous and detail-oriented assistant.",
            "You are a relaxed and easygoing assistant.",
            "You are an energetic and enthusiastic assistant.",
            "You are a no-nonsense and direct assistant.",
            "You are a supportive and encouraging assistant.",
            "You are a formal and respectful assistant.",
            # Less professional and fun personalities
            "You are a quirky and eccentric assistant.",
            "You are a sarcastic and witty assistant.",
            "You are a laid-back and chill assistant.",
            "You are a mischievous and playful assistant.",
            "You are an overly enthusiastic assistant.",
            "You are a nerdy and geeky assistant.",
            "You are a dramatic and theatrical assistant.",
            "You are a rebellious and edgy assistant.",
            "You are a cool and hip assistant.",
            "You are a dreamy and whimsical assistant.",
            "You are a sassy and a tad mean assistant.",
        ]
        personality = random.choice(personalities)
        IntentsService.set_personality(personality)

    @staticmethod
    def set_personality_from_openai():
        """
        Sets the personality of the assistant using a response from the OpenAI API.
        """
        prompt = "Please provide a personality description for an AI assistant that can be used as a system role."
        personality = IntentsService.get_ai_response(
            prompt=prompt,
            system_role="You are an AI model providing personality descriptions for assistants.",
        )
        IntentsService.set_personality(personality)

    @staticmethod
    def get_ai_response(
        prompt: str, model_identifier: str = None, system_role: str = None
    ) -> str:
        """
        Helper method to get response from AIService.

        Args:
            prompt (str): The input prompt for the API.
            model_identifier (str, optional): The model identifier to use for the request. Defaults to IntentsService.model_identifier.
            system_role (str, optional): The system role to include in the request. Defaults to IntentsService.system_role.

        Returns:
            str: The response text from the AIService.
        """
        if model_identifier is None:
            model_identifier = IntentsService.model_identifier

        if IntentsService.system_role is None:
            IntentsService.set_random_personality()

        if system_role is None:
            system_role = IntentsService.system_role

        ai_service = AIServiceSingleton.get_instance()
        response_text = ai_service.get_response_with_model_name(
            prompt, model_identifier, system_role
        )
        logger.info("Response for prompt '%s': %s", prompt, response_text)
        return response_text

    @staticmethod
    def handle_request(payload):
        query = payload["request"]
        prompt = render_template("query_prompt", query=query)
        response_text = IntentsService.get_ai_response(prompt)
        return {"type": "statement", "response": response_text}

    @staticmethod
    def get_launch_message():
        IntentsService.set_random_personality()
        prompt = render_template("launch_prompt")
        response_text = IntentsService.get_ai_response(
            prompt, IntentsService.model_identifier, IntentsService.system_role
        )
        return {"type": "question", "response": response_text}

    @staticmethod
    def get_fallback_message():
        prompt = render_template("fallback_prompt")
        response_text = IntentsService.get_ai_response(prompt)
        return {"type": "question", "response": response_text}

    @staticmethod
    def get_goodbye_message():
        prompt = render_template("goodbye_prompt")
        response_text = IntentsService.get_ai_response(prompt)
        return {"type": "statement", "response": response_text}

    @staticmethod
    def get_help_message():
        prompt = render_template("help_prompt")
        response_text = IntentsService.get_ai_response(prompt)
        return {"type": "question", "response": response_text}

    @staticmethod
    def get_stop_message():
        prompt = render_template("stop_prompt")
        response_text = IntentsService.get_ai_response(prompt)
        return {"type": "statement", "response": response_text}

    @staticmethod
    def get_cancel_message():
        prompt = render_template("cancel_prompt")
        response_text = IntentsService.get_ai_response(prompt)
        return {"type": "statement", "response": response_text}

    @staticmethod
    def get_session_ended_message():
        prompt = render_template("session_ended_prompt")
        response_text = IntentsService.get_ai_response(prompt)
        return {"type": "statement", "response": response_text}

    @staticmethod
    def handle_weather_forecast(payload):

        service = WeatherService()

        slot_info = payload["request"]
        prompt = service.handle_weather_forecast(slot_info)

        # query = "weather for today"  # payload["request"]
        # prompt = render_template("query_prompt", query=query)
        response_text = IntentsService.get_ai_response(prompt)
        return {"type": "statement", "response": response_text}
