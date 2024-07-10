import logging
from functools import wraps

import openai

from app.config.config import Config
from app.helpers.resource_loader import ResourceLoader
from app.models.ai.model_config import ModelConfig
from app.models.ai.model_configs import ModelConfigs

# from app.utilities import ResourceLoader

# Configure logging
logger = logging.getLogger(__name__)


class AIService:
    """
    Service class for interacting with the OpenAI API.

    This class provides methods to interact with the OpenAI API, including fetching responses for given prompts
    with optimization techniques like memoization and parallel processing.
    """

    def __init__(self, config_path: str):
        """
        Initializes the AIService with the provided model configurations.

        Args:
            config_path (str): Path to the model configuration file.
        """
        self.config = Config()
        self.model_configs = self.load_configs(config_path)

    @staticmethod
    def load_configs(config_path: str) -> ModelConfigs:
        """
        Loads model configurations from a JSON file.

        Args:
            config_path (str): Path to the model configuration file.

        Returns:
            ModelConfigs: An instance of ModelConfigs with loaded configurations.
        """
        configs = ResourceLoader.load_json_file(config_path)
        return ModelConfigs(configs=configs)

    @staticmethod
    def memoize(func):
        """
        Decorator to memoize function results.

        Args:
            func (callable): The function to memoize.

        Returns:
            callable: The memoized function.
        """
        cache = {}

        @wraps(func)
        def memoized_func(*args, **kwargs):
            key = (args, tuple(kwargs.items()))
            if key not in cache:
                logger.info("Cache miss for key: %s", key)
                cache[key] = func(*args, **kwargs)
            else:
                logger.info("Cache hit for key: %s", key)
            return cache[key]

        return memoized_func

    def get_model_config(self, model_name: str) -> ModelConfig:
        """
        Retrieves a specific model configuration by model name.

        Args:
            model_name (str): The name of the model to retrieve.

        Returns:
            ModelConfig: The model configuration matching the model name.
        """
        for config in self.model_configs.configs:
            if config.model == model_name:
                return config
        raise ValueError(f"Model {model_name} not found in the configurations.")

    # @memoize
    def get_openai_response(
        self, prompt, model_config: ModelConfig, system_role: str = None
    ):
        """
        Fetches response from OpenAI API for a given prompt using a specified model configuration and optional system role.

        Args:
            prompt (str): The input prompt for the API.
            model_config (ModelConfig): The model configuration to use for the request.
            system_role (str, optional): The system role to include in the request.

        Returns:
            str: The response text from OpenAI API.
        """
        client = openai.OpenAI(
            base_url=model_config.base_url,
            api_key=model_config.api_key,
        )

        messages = []
        if system_role:
            messages.append({"role": "system", "content": system_role})
        messages.append({"role": "user", "content": prompt})

        try:
            response = client.chat.completions.create(
                model=model_config.model,
                messages=messages,
            )
            return response.choices[0].message.content.strip()
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")

    def get_response_with_model_name(
        self, prompt: str, model_name: str, system_role: str = None
    ) -> str:
        """
        Fetches response from OpenAI API for a given prompt using the specified model name and optional system role.

        Args:
            prompt (str): The input prompt for the API.
            model_name (str): The name of the model to use for the request.
            system_role (str, optional): The system role to include in the request.

        Returns:
            str: The response text from OpenAI API.
        """
        model_config = self.model_configs.get_model_config(model_name)
        return self.get_openai_response(prompt, model_config, system_role)

    # def generate(self, prompt, model=None, options=None):
    #     model_to_use = self.model if not model else model
    #     response = None
    #     status_code = 0
    #     status = "OK"
    #     generate_respone = None
    #     logging.info("Generate for model: %s.", model_to_use)
    #     try:
    #         response = self.client.generate(
    #             model=model_to_use, prompt=prompt, format="json", options=options
    #         )
    #         if not response:  # or not response.valid:
    #             status_code = -1
    #             status = "Unknown error in api"
    #             logging.error("Unknown error in api")
    #         else:
    #             generate_respone = response["response"]

    #     except ResponseError as re:
    #         status_code = -1
    #         status = re.error
    #         logging.error("Error in api: %s", status)

    #     api_response = {
    #         "status": status,
    #         "status_code": status_code,
    #         "response": generate_respone,
    #     }
    #     return api_response

    # def create_prompt(self, email_details):
    #     """Construct the prompt for the AI analysis based on the newsletter content."""
    #     try:
    #         with open(email_details["body"], "r", encoding="UTF-8") as file:
    #             newsletter_content = file.read()
    #     except FileNotFoundError:
    #         logging.error("Newsletter file %s not found", email_details["body"])
    #         return ""

    #     try:
    #         with open(
    #             os.getenv("NEWSLETTER_TICKERS_PROMPT"), "r", encoding="UTF-8"
    #         ) as file:
    #             authority_prompt = file.read()
    #     except FileNotFoundError:
    #         logging.error("Newsletter tickers prompt file not found")
    #         return ""

    #     return authority_prompt + "\n" + newsletter_content


# def main():
#     api = AIService()
#     print(json.dumps(api.generate("What is the capital of Luxembourg?"), indent=2))
#     # print(json.dumps(api.generate("What is the capital of Luxembourg?"), indent=2))


# if __name__ == "__main__":
#     main()
