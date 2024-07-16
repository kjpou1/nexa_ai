import json
import logging
from datetime import datetime
from typing import Any, Dict, Optional

from app.apis.open_weather_map_api import OpenWeatherMapAPI
from app.config.config import Config
from app.helpers.weather_helpers import WeatherHelpers

# Set up logging
logger = logging.getLogger(__name__)


class WeatherService:
    """
    A service class to handle weather forecast processing.
    """

    def __init__(self, api_key: Optional[str] = None):

        if api_key is None:
            api_key = Config.get("OPEN_WEATHER_MAP_KEY")

        self.api = OpenWeatherMapAPI(api_key)
        self.config = Config()

    def handle_weather_forecast(self, slots: Dict[str, Any]) -> str:
        """
        Handle the weather forecast by retrieving weather parameters from the slots object
        and creating a human-readable OpenAI prompt.

        Parameters:
        slots (Dict[str, Any]): Dictionary containing slot data.

        Returns:
        str: Human-readable weather forecast response.
        """
        # Extract weather parameters from slots
        weather_params = WeatherHelpers.get_weather_parameters(slots)

        # Determine location
        location = WeatherHelpers.determine_location(weather_params)
        lat = 0
        lon = 0

        if location == self.config.public_location:
            ip_info = self.config.public_ip_info
            lat = ip_info.latitude
            lon = ip_info.longitude
        else:
            # Geocode the location to get latitude and longitude
            geocode_data = WeatherHelpers.geocode_location(location, self.api)
            lat = geocode_data.get("lat")
            lon = geocode_data.get("lon")

        # Fetch weather data from OpenWeatherMap API
        # weather_data = self.api.get_weather(lat, lon)
        # # Create OpenAI prompt to format the weather information
        # # openai_prompt = WeatherHelpers.create_openai_prompt(
        # #     weather_params, weather_data=weather_data
        # # )
        # date = "2024-07-11"
        # openai_prompt = WeatherHelpers.generate_detailed_prompt(
        #     weather_data=weather_data, date=date
        # )
        # Fetch weather data from OpenWeatherMap API
        weather_overview = self.api.get_overview(lat, lon)

        openai_prompt = WeatherHelpers.generate_overview_prompt(
            overview_data=weather_overview
        )

        # Return the OpenAI prompt
        return openai_prompt

    def get_weather_forecast(
        self,
        duration: str = "today",
        location: str = None,
        start_date: str = None,
        weather_condition: str = None,
    ) -> str:
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
                            Defaults to public ip_location if not provided.
                            Examples:
                            - "Nags Head"
                            - "Luxembourg, LU"
                            - "New York, US"

            start_date (str): Optional string specifying the start date for the weather forecast in the format 'YYYY-MM-DD'.
                              Defaults to today's date if not provided.

            weather_condition (str): Optional string specifying the type of weather condition to filter the forecast by.
                                     Examples: "rain", "snow", "fog".
                                     If not provided, forecasts for all weather conditions will be returned.

        Returns:
            str: The weather data for the specified duration, location, start date, and weather condition.

        Raises:
            ValueError: If an unsupported duration value or invalid date is provided.

        Example:
            >>> weather_service.get_weather_forecast("today", "Nags Head", "2023-07-14", "rain")
            'The weather forecast for Nags Head starting on 2023-07-14 for today is: rain with a temperature of 22°C.'
        """
        if location is None:
            location = self.config.public_location  # Default location if none provided

        if duration not in ["today", "tomorrow", "week"]:
            raise ValueError(
                "Unsupported duration value. Accepted values are 'today', 'tomorrow', and 'week'."
            )

        if start_date is None:
            start_date = datetime.now().strftime(
                "%Y-%m-%d"
            )  # Default to today's date if not provided

        try:
            datetime.strptime(start_date, "%Y-%m-%d")  # Validate date format
        except ValueError:
            raise ValueError("Invalid date format. Expected format is 'YYYY-MM-DD'.")

        # params = {
        #     'q': location,
        #     'appid': self.api_key,
        #     'units': 'metric',
        #     'cnt': 7  # Limit to 7 days of forecast data
        # }

        try:
            # Determine location
            lat = 0
            lon = 0

            if location == self.config.public_location:
                ip_info = self.config.public_ip_info
                lat = ip_info.latitude
                lon = ip_info.longitude
            else:
                # Geocode the location to get latitude and longitude
                geocode_data = WeatherHelpers.geocode_location(location, self.api)
                lat = geocode_data.get("lat")
                lon = geocode_data.get("lon")

            weather_overview = self.api.get_overview(lat, lon)

            openai_prompt = WeatherHelpers.generate_overview_prompt(
                overview_data=weather_overview
            )
            # response = requests.get(self.base_url, params=params, timeout=10)
            # response.raise_for_status()
            # weather_data = response.json()

            # # Extract relevant data from the response
            # forecasts = weather_data.get('list', [])
            # forecast_text = []
            # for forecast in forecasts:
            #     date_text = forecast.get('dt_txt', '')
            #     date = datetime.strptime(date_text, '%Y-%m-%d %H:%M:%S')
            #     if date.strftime('%Y-%m-%d') == start_date:
            #         weather_desc = forecast.get('weather', [{}])[0].get('description', 'No description available')
            #         if weather_condition and weather_condition.lower() not in weather_desc.lower():
            #             continue  # Skip this forecast if it does not match the weather condition
            #         temp = forecast.get('main', {}).get('temp', 'No temperature available')
            #         forecast_text.append(f"{date_text}: {weather_desc} with a temperature of {temp}°C")

            # if not forecast_text:
            #     return f"No forecast data for {weather_condition} found on {start_date} in {location}."
            forecast_text = "Not Now"
            result = (
                f"The weather forecast for {location} starting on {start_date} for {duration} is:\n"
                + "\n".join(forecast_text)
            )
            logger.info("Weather data fetched successfully.")
            result = openai_prompt

            return result

        except ValueError as e:
            logger.error("Error fetching weather data: %s", e)
            return "Error fetching weather data."
