import logging
import re
from datetime import datetime

from app.models.intent_response import IntentResponse, IntentResponseDetails
from app.services.ai.ai_service_instance import AIServiceSingleton
from app.services.browser.browser_service import BrowserService
from app.services.weather.weather_service import WeatherService


class ActionExecutorService:
    """
    Service to execute a given function string.

    Attributes:
        function_map (dict): A mapping of function names to their corresponding functions.

    Methods:
        execute_function(function_str: str) -> str: Executes the given function string and returns the result.
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.weather_service = WeatherService()
        self.web_service = BrowserService()
        self.ai_service = AIServiceSingleton.get_instance()
        self.function_map = {
            "get_weather_forecast": self.weather_service.get_weather_forecast,
            "ask_the_ai": self.ai_service.ask_the_ai,
            "web_search": self.web_service.web_search,
        }

    def execute_function(self, function_str: str) -> IntentResponse:
        """
        Executes the given function string by extracting the function name and arguments,
        then using a controlled environment to call the function.

        Parameters:
            function_str (str): The function call string to be executed.

        Returns:
            IntentResponse: The structured IntentResponse dataclass.

        Example:
            executor = ActionExecutorService()
            result = executor.execute_function("Call: get_weather_forecast(duration='today')")
            print(result)
        """
        self.logger.info("Executing function: %s", function_str)

        # Extract function name and arguments
        match = re.match(r"Call:\s*(\w+)\((.*)\)", function_str)
        if not match:
            self.logger.error("Invalid function call format")
            return IntentResponse(
                request=function_str,
                details=IntentResponseDetails(
                    status="failure",
                    data="Invalid function call format",
                    timestamp=datetime.now().isoformat(),
                ),
            )

        func_name = match.group(1)
        func_args = match.group(2)

        if func_name not in self.function_map:
            self.logger.error("Function %s is not allowed", func_name)
            return IntentResponse(
                request=function_str,
                details=IntentResponseDetails(
                    status="failure",
                    data=f"Function {func_name} is not allowed",
                    timestamp=datetime.now().isoformat(),
                ),
            )

        try:
            func = self.function_map[func_name]
            # Convert the argument string into a dictionary
            args_dict = eval(f"dict({func_args})")
            func_result = func(**args_dict)
            self.logger.info("Function executed successfully")
            return IntentResponse(
                request=function_str,
                details=IntentResponseDetails(
                    status="success",
                    data=func_result,
                    timestamp=datetime.now().isoformat(),
                ),
            )
        except Exception as e:
            self.logger.error("Error executing function: %s", e)
            return IntentResponse(
                request=function_str,
                details=IntentResponseDetails(
                    status="failure", data=str(e), timestamp=datetime.now().isoformat()
                ),
            )


# Example usage
if __name__ == "__main__":
    executor = ActionExecutorService()
    result = executor.execute_function("Call: get_weather_forecast(duration='today')")
    logging.info("Execution result: %s", result)

    # Example with different arguments
    result = executor.execute_function(
        "Call: get_weather_forecast(duration='week', weather_condition='snow')"
    )
    logging.info("Execution result: %s", result)
