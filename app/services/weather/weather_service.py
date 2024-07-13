import json
import logging
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
