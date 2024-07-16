import logging
from datetime import datetime

from app.models.intent_response import IntentResponse, IntentResponseDetails


class ActionResponseService:
    """
    Service to format the response after executing a function.

    Methods:
        format_response(response: dict) -> str: Formats the given response dictionary.
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def format_response(self, response: IntentResponse) -> IntentResponse:
        """
        Formats the given response dataclass. The dataclass must contain
        'request' and 'details' fields.

        Parameters:
            response (IntentResponse): The response dataclass to be formatted.

        Returns:
            IntentResponse: The formatted response dataclass.

        Example:
            response_service = ActionResponseService()
            response_data = IntentResponse(
                request="get_weather_forecast",
                details=IntentResponseDetails(
                    status="success",
                    data="The weather forecast for Luxembourg is sunny with a temperature of 22°C.",
                    timestamp="2023-07-14T10:00:00Z"
                )
            )
            formatted_response = response_service.format_response(response_data)
            print(formatted_response)
        """
        self.logger.info("Formatting response")

        try:
            request = response.request
            details = response.details
            status = details.status
            data = details.data
            timestamp = details.timestamp
        except AttributeError as e:
            self.logger.error("Missing attribute in response dataclass: %s", e)
            return IntentResponse(
                request=response.request,
                details=IntentResponseDetails(
                    status="failure",
                    data="Invalid response format",
                    timestamp=datetime.now().isoformat(),
                ),
            )

        # Additional formatting can be added here if needed
        intent_response = IntentResponse(
            request=request,
            details=IntentResponseDetails(
                status=status, data=data, timestamp=timestamp
            ),
        )
        return intent_response


# Example usage
if __name__ == "__main__":
    response_service = ActionResponseService()
    response_data = IntentResponse(
        request="get_weather_forecast",
        details=IntentResponseDetails(
            status="success",
            data="The weather forecast for Luxembourg is sunny with a temperature of 22°C.",
            timestamp="2023-07-14T10:00:00Z",
        ),
    )
    formatted_response = response_service.format_response(response_data)
    logging.info("Formatted response: %s", formatted_response)
