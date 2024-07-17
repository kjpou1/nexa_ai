import logging

import openai
from flask import render_template
from openai import OpenAI

from app.config.config import Config
from app.helpers.resource_loader import ResourceLoader
from app.models.ai.model_config import ModelConfig
from app.models.ai.model_configs import ModelConfigs


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
        # Configure logging
        self.logger = logging.getLogger(__name__)

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

    # @staticmethod
    # def memoize(func):
    #     """
    #     Decorator to memoize function results.

    #     Args:
    #         func (callable): The function to memoize.

    #     Returns:
    #         callable: The memoized function.
    #     """
    #     cache = {}

    #     @wraps(func)
    #     def memoized_func(*args, **kwargs):
    #         key = (args, tuple(kwargs.items()))
    #         if key not in cache:
    #             self.logger.info("Cache miss for key: %s", key)
    #             cache[key] = func(*args, **kwargs)
    #         else:
    #             self.logger.info("Cache hit for key: %s", key)
    #         return cache[key]

    #     return memoized_func

    def get_model_config(self, model_name: str) -> ModelConfig:
        """
        Retrieves a specific model configuration by model name.

        Args:
            model_name (str): The name of the model to retrieve.

        Returns:
            ModelConfig: The model configuration matching the model name.
        """
        config_model = self.model_configs.get_model_config(model_name)
        if config_model:
            return config_model
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

    def get_raven_function_response(
        self,
        prompt,
        model_config: ModelConfig,
    ):

        RAVEN_PROMPT = '''
        <human>:
        Function:
        def ask_the_ai(query: str) -> str:
            """
            The user's non modified query does not contain the words 'web' or 'internet'
            
            Args:
                query (str): The snon modified earch query string provided by the user where there is no specific referenct to use 'web' or 'internet'

            Returns:
                str: A comprehensive response generated by ai.
            """

        Function:
        def web_search(search: str) -> str:
            """
            The user's non modified search contains the words 'web' or 'internet'

            Args:
                search (str): The non modified search string provided by the user where the search contains the words 'web' or 'internet' specifically.

            Returns:
                str: A comprehensive response generated by web or internet.
            """

        Function:
        def get_weather_forecast(duration: str = "today", location: str = None, start_date: str = None, weather_condition: str = None) -> str:
            """
            Fetches weather data from the service API for the given duration starting from a specific date and filtered by weather condition.

            Args:
                duration (str): Specifies when the weather forecast is for.
                                Accepted values are:
                                - "today": Retrieves the weather forecast for the current day.
                                - "tomorrow": Retrieves the weather forecast for the next day.
                                - "week": Retrieves the weather forecast for the upcoming week.
                                Note: If the weather service API does not support forecasts beyond today, 
                                the function will return the forecast for today.
                                Defaults to "today" if not provided.
                                
                location (str): Optional string specifying the location for the weather forecast. 
                                Can be a city name, city name and country code, or city name and state code.
                                Defaults to 'London' if not provided.
                                Examples: 
                                - "Nags Head"
                                - "Paris, FR"
                                - "New York, US"
                                
                start_date (str): Optional string specifying the start date for the weather forecast in the format 'YYYY-MM-DD'.
                                Defaults to today's date if not provided.

                weather_condition (str): Optional string specifying the type of weather condition to filter the forecast by.
                                 Examples: "rain", "snow", "fog".
                                 If not provided, forecasts for all weather conditions will be returned.

                Returns:
                    str: The weather data for the specified duration, location, start date, and weather condition.
                        
            """

        Function:
        def get_weather_temperature(when):
            """
            Fetches weather temperature from the service API for the given duration.

            Args:
            when : When is the temperature for: example ...for today

            Returns:
            str: The temperature data for when 
            """

        User Query: {query}

        Please pick a function from the above function definitions that best answers the 
        user query and fill in the appropriate arguments.
        <human_end>
        '''

        try:

            question = prompt

            prompt_content = RAVEN_PROMPT.format(query=question)

            messages = []
            messages.append({"role": "user", "content": prompt_content})

            client = OpenAI(
                base_url=model_config.base_url,
                api_key=model_config.api_key,
            )
            response = client.chat.completions.create(
                model=model_config.model,
                messages=messages,
                stream=False,
                temperature=0.001,
                stop="<bot_end>",
            )
            response_message = response.choices[0].message
            return response_message.content
        except Exception as e:
            print(f"An error occurred: {e}")
            for ss in messages:
                message_stuff = f'Role: {ss["role"]}\nContent:{ss["content"]}\n'
                print(message_stuff)

        return None

    def get_function_for_utterance(self, utterance: str) -> str:
        """
        Calls the OpenAI API to get a function call string based on the given utterance.

        Parameters:
            utterance (str): The user's input as a string.

        Returns:
            str: The function call string interpreted from the utterance.

        Example:
            ai_service = AIService()
            function_str = ai_service.get_function_for_utterance('weather for today')
            print(function_str)
        """
        self.logger.info("Calling OpenAI API for utterance: %s", utterance)
        model = self.get_model_config("nexus")
        response = self.get_raven_function_response(utterance, model_config=model)
        self.logger.info("Utterance function: %s", response)
        return response

    def ask_the_ai(self, query: str) -> str:
        """
        The user's non modified query does not contain the words 'web' or 'internet'

        Args:
            query (str): The snon modified earch query string provided by the user where there is no specific referenct to use 'web' or 'internet'

        Returns:
            str: A comprehensive response generated by ai.
        """
        model_identifier = self.config.large_language_model
        system_role = self.config.personality

        prompt = render_template("query_prompt", query=query)
        response_text = self.get_response_with_model_name(
            prompt, model_identifier, system_role
        )
        self.logger.info("Response for prompt '%s': %s", prompt, response_text)
        return response_text

    def prompt_the_ai(self, prompt: str) -> str:
        """
        The user's non modified query does not contain the words 'web' or 'internet'

        Args:
            query (str): The snon modified earch query string provided by the user where there is no specific referenct to use 'web' or 'internet'

        Returns:
            str: A comprehensive response generated by ai.
        """
        model_identifier = self.config.large_language_model
        system_role = self.config.personality

        response_text = self.get_response_with_model_name(
            prompt, model_identifier, system_role
        )
        self.logger.info("Response for prompt '%s': %s", prompt, response_text)
        return response_text


# def main():
#     api = AIService()
#     print(json.dumps(api.generate("What is the capital of Luxembourg?"), indent=2))
#     # print(json.dumps(api.generate("What is the capital of Luxembourg?"), indent=2))


# if __name__ == "__main__":
#     main()
