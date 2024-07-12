import logging
from typing import Any, Dict

import requests

from app.config.config import Config

# Set up logging
logger = logging.getLogger(__name__)


class OpenWeatherMapAPI:
    """
    A class to interact with the OpenWeatherMap API.
    """

    GEOCODE_URL = "http://api.openweathermap.org/geo/1.0/direct"
    WEATHER_URL = "https://api.openweathermap.org/data/3.0/onecall"

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.config = Config()

    def geocode_location(self, location: str) -> Dict[str, Any]:
        """
        Geocode a location to get latitude and longitude.

        Parameters:
        location (str): The location to geocode.

        Returns:
        Dict[str, Any]: Geocoded location data.
        """
        params = {"q": location, "units": self.config.units, "appid": self.api_key}
        try:
            headers = {"Content-Type": "application/json"}
            response = requests.get(
                self.GEOCODE_URL, params=params, headers=headers, timeout=10
            )
            # logger.info(response.url)
            response.raise_for_status()
            data = response.json()
            if data:
                logger.info("Geocoded location data retrieved successfully: %s", data)
                return data[0]
            else:
                logger.error("No geocoding data found for location: %s", location)
                return {}
        except requests.RequestException as e:
            logger.error(
                "Error fetching geocoding data from OpenWeatherMap", exc_info=True
            )
            raise e

    def get_weather(self, lat: float, lon: float) -> Dict[str, Any]:
        """
        Fetch weather data for a specified latitude and longitude.

        Parameters:
        lat (float): Latitude.
        lon (float): Longitude.

        Returns:
        Dict[str, Any]: Weather data.
        """
        params = {
            "lat": lat,
            "lon": lon,
            "units": Config().units,
            "appid": self.api_key,
        }
        try:
            response = requests.get(self.WEATHER_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            # logger.info("Weather data retrieved successfully: %s", data)
            return data
        except requests.RequestException as e:
            logger.error(
                "Error fetching weather data from OpenWeatherMap", exc_info=True
            )
            raise e
