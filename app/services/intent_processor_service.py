import logging
import random
from datetime import datetime

from app.config.config import Config
from app.models.intent_response import IntentResponse, IntentResponseDetails
from app.models.singleton import SingletonMeta
from app.services.ai.ai_service_instance import AIServiceSingleton
from app.services.execution.action_executor_service import ActionExecutorService
from app.services.formatting.action_response_service import ActionResponseService


class IntentProcessorService(metaclass=SingletonMeta):
    """
    Service to process user utterances by calling the AI service to interpret the
    utterance, executing the returned function, and formatting the response.

    Attributes:
        ai_service (AIService): Instance of AIService to get function calls.
        action_executor_service (ActionExecutorService): Instance of ActionExecutorService to execute functions.
        action_response_service (ActionResponseService): Instance of ActionResponseService to format the response.
        system_role (str): The personality description for the assistant.
    """

    _is_initialized = False

    def __init__(self):
        if not self._is_initialized:  # Prevent reinitialization
            self.logger = logging.getLogger(__name__)
            self.config = Config()
            self.ai_service = AIServiceSingleton.get_instance()
            self.action_executor_service = ActionExecutorService()
            self.action_response_service = ActionResponseService()
            self.system_role = None
            self._is_initialized = True

    @classmethod
    def initialize(cls):
        """
        Convenience method to explicitly initialize the IntentProcessorService
        """
        cls()

    def set_personality(self, personality: str):
        """
        Sets the personality of the assistant for the system role.

        Args:
            personality (str): The personality description for the assistant.
        """
        self.system_role = personality
        self.config.set_personality(personality)
        self.logger.info("System role set to: %s", personality)

    def set_random_personality(self):
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
        self.set_personality(personality)

    def set_personality_from_openai(self):
        """
        Sets the personality of the assistant using a response from the OpenAI API.
        """
        prompt = "Please provide a personality description for an AI assistant that can be used as a system role."
        personality = self.get_ai_response(
            prompt=prompt,
            system_role="You are an AI model providing personality descriptions for assistants.",
        )
        self.set_personality(personality)

    def get_ai_response(
        self, prompt: str, model_identifier: str = None, system_role: str = None
    ) -> str:
        """
        Helper method to get response from AIService.

        Args:
            prompt (str): The input prompt for the API.
            model_identifier (str, optional): The model identifier to use for the request. Defaults to a preset identifier.
            system_role (str, optional): The system role to include in the request. Defaults to the instance's system_role.

        Returns:
            str: The response text from the AIService.
        """
        if model_identifier is None:
            model_identifier = "llama3"  # Default model identifier

        if self.system_role is None:
            self.set_random_personality()

        if system_role is None:
            system_role = self.system_role

        response_text = self.ai_service.get_response_with_model_name(
            prompt, model_identifier, system_role
        )
        self.logger.info("Response for prompt '%s': %s", prompt, response_text)
        return response_text

    def process_utterance(self, utterance: str) -> IntentResponse:
        """
        Processes the given utterance by calling the AI service, executing the returned
        function, and formatting the response.

        Parameters:
            utterance (str): The user's input as a string.

        Returns:
            IntentResponse: The formatted response after processing the utterance.

        Example:
            processor = IntentProcessorService()
            response = processor.process_utterance('weather for today')
            print(response)
        """
        self.logger.info("Processing utterance: %s", utterance)
        try:
            function_str = self.ai_service.get_function_for_utterance(utterance)
            self.logger.debug("Function string received: %s", function_str)

            if function_str:
                result = self.action_executor_service.execute_function(function_str)
                self.logger.debug("Result of function execution: %s", result)

                formatted_response = self.action_response_service.format_response(
                    result
                )
                self.logger.info("Formatted response: %s", formatted_response)

                return formatted_response
            else:
                self.logger.error(
                    "No valid function returned for the utterance: %s", utterance
                )
                return IntentResponse(
                    request=utterance,
                    details=IntentResponseDetails(
                        status="failure",
                        data="No valid function returned for the utterance",
                        timestamp=datetime.now().isoformat(),
                    ),
                )
        except Exception as e:
            self.logger.exception(
                "Exception occurred while processing utterance: %s", utterance
            )
            return IntentResponse(
                request=utterance,
                details=IntentResponseDetails(
                    status="error",
                    data=str(e),
                    timestamp=datetime.now().isoformat(),
                ),
            )
