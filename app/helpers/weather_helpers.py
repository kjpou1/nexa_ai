import datetime
import json
import logging
from typing import Any, Dict, Optional

from app.apis.ip_resolver import IPResolver
from app.apis.open_weather_map_api import OpenWeatherMapAPI
from app.config.config import Config

# Set up logging
logger = logging.getLogger(__name__)


class WeatherHelpers:
    """
    A static class offering weather-related utilities for formatting, parsing, etc.
    """

    @staticmethod
    def parse_json_string(json_string: str) -> Dict[str, Any]:
        """
        Parse a JSON string and return the parsed JSON data.

        Parameters:
        json_string (str): JSON string to parse.

        Returns:
        Dict[str, Any]: Parsed JSON data.
        """
        try:
            data = json.loads(json_string)
            logger.info("Successfully parsed JSON string")
            return data
        except json.JSONDecodeError as e:
            logger.error("Error parsing JSON string", exc_info=True)
            raise e

    @staticmethod
    def extract_field(data: Dict[str, Any], field_name: str) -> Optional[str]:
        """
        Extract a specific field value from the dictionary.

        Parameters:
        data (Dict[str, Any]): Dictionary containing data.
        field_name (str): The name of the field to extract.

        Returns:
        Optional[str]: The extracted field value or None if the field is not found.
        """
        field = data.get(field_name)
        if field and "value" in field:
            return field["value"]
        logger.warning("Field %s not found or missing value", field_name)
        return None

    @staticmethod
    def get_weather_parameters(data: Dict[str, Any]) -> Dict[str, Optional[str]]:
        """
        Extract necessary parameters for weather information from JSON data.

        Parameters:
        data (Dict[str, Any]): Parsed JSON data.

        Returns:
        Dict[str, Optional[str]]: Dictionary containing weather parameters.
        """
        weather_params = {
            "start_date": WeatherHelpers.extract_field(data, "object.startDate"),
            "weather_condition": WeatherHelpers.extract_field(
                data, "object.weatherCondition.name"
            ),
            "location_locality": WeatherHelpers.extract_field(
                data, "object.location.addressLocality.name"
            ),
            "location_region": WeatherHelpers.extract_field(
                data, "object.location.addressRegion.name"
            ),
            "location_country": WeatherHelpers.extract_field(
                data, "object.location.addressCountry.name"
            ),
        }
        logger.info("Extracted weather parameters: %s", weather_params)
        return weather_params

    @staticmethod
    def determine_location(weather_params: Dict[str, Optional[str]]) -> str:
        """
        Determine the location from weather parameters or IP resolver.

        Parameters:
        weather_params (Dict[str, Optional[str]]): Dictionary containing weather parameters.

        Returns:
        str: The determined location.
        """
        location_parts = filter(
            None,
            [
                weather_params.get("location_locality"),
                weather_params.get("location_region"),
                weather_params.get("location_country"),
            ],
        )
        location = ", ".join(location_parts) if location_parts else None

        if not location:
            # Resolve location based on IP if not provided in weather parameters
            location = Config().public_location

        return location

    @staticmethod
    def geocode_location(location: str, api: OpenWeatherMapAPI) -> Dict[str, float]:
        """
        Geocode the location to get latitude and longitude.

        Parameters:
        location (str): The location to geocode.
        api (OpenWeatherMapAPI): Instance of OpenWeatherMapAPI to use for geocoding.

        Returns:
        Dict[str, float]: Dictionary containing latitude and longitude.
        """
        geocode_data = api.geocode_location(location)
        lat = geocode_data.get("lat")
        lon = geocode_data.get("lon")

        if not lat or not lon:
            logger.error("Geocoding failed for location: %s", location)
            raise ValueError(f"Geocoding failed for location: {location}")

        return {"lat": lat, "lon": lon}

    @staticmethod
    def create_openai_prompt(
        weather_params: Dict[str, Optional[str]], weather_data: Dict[str, Any]
    ) -> str:
        """
        Create an OpenAI prompt to format the weather information into a human-readable response.

        Parameters:
        weather_params (Dict[str, Optional[str]]): Dictionary containing weather parameters.
        weather_data (Dict[str, Any]): Dictionary containing weather data from the API.

        Returns:
        str: OpenAI prompt string.
        """
        start_date = weather_params.get("start_date", "an unknown date")
        weather_condition = weather_params.get(
            "weather_condition", "unknown weather conditions"
        )
        location_parts = filter(
            None,
            [
                weather_params.get("location_locality"),
                weather_params.get("location_region"),
                weather_params.get("location_country"),
            ],
        )
        location = (
            ", ".join(location_parts) if location_parts else "an unknown location"
        )

        current_weather = weather_data.get("current", {})
        temp = current_weather.get("temp", "unknown temperature")
        description = current_weather.get("weather", [{}])[0].get(
            "description", "unknown conditions"
        )

        prompt = (
            f"The weather forecast for {location} on {start_date} indicates {weather_condition}. "
            f"The current temperature is {temp}K with {description}. "
            "Please format this information into a human-readable response."
        )
        logger.info("Created OpenAI prompt: %s", prompt)
        return prompt

    @staticmethod
    def generate_prompt(weather_data: Dict[str, Any], date: str) -> str:
        """Generate a detailed weather forecast prompt."""
        current = weather_data["current"]
        daily = weather_data["daily"][0]
        hourly = weather_data["hourly"][:3]

        location = weather_data.get("timezone", "an unknown location").split("/")[1]

        current_temp = current["temp"]
        feels_like_temp = current["feels_like"]
        current_conditions = current["weather"][0]["description"]
        current_humidity = current["humidity"]
        current_wind_speed = current["wind_speed"]
        current_wind_deg = current["wind_deg"]
        current_visibility = current["visibility"]
        current_pressure = current["pressure"]
        current_uvi = current["uvi"]

        sunrise = datetime.datetime.fromtimestamp(daily["sunrise"]).strftime("%I:%M %p")
        sunset = datetime.datetime.fromtimestamp(daily["sunset"]).strftime("%I:%M %p")
        max_temp = daily["temp"]["max"]
        min_temp = daily["temp"]["min"]
        daily_conditions = daily["weather"][0]["description"]
        daily_summary = daily.get("summary", "No summary available.")
        daily_humidity = daily["humidity"]
        daily_wind_speed = daily["wind_speed"]
        daily_wind_deg = daily["wind_deg"]
        daily_rain = daily.get("rain", 0)
        daily_uvi = daily["uvi"]

        hourly_forecast = []
        for hour in hourly:
            time = datetime.datetime.fromtimestamp(hour["dt"]).strftime("%I:%M %p")
            temp = hour["temp"]
            conditions = hour["weather"][0]["description"]
            humidity = hour["humidity"]
            wind_speed = hour["wind_speed"]
            wind_deg = hour["wind_deg"]
            hourly_forecast.append(
                f"1. **Time:** {time}\n"
                f"   - Temperature: {temp:.2f}\n"
                f"   - Conditions: {conditions}\n"
                f"   - Humidity: {humidity}%\n"
                f"   - Wind Speed: {wind_speed} m/s from {wind_deg} degrees"
            )

        prompt = (
            # f"Provide a detailed weather forecast for the following location and date, incorporating current weather conditions, "
            f"Provide a detailed  weather forecast for {location} on {date}, incorporating current weather conditions, "
            f"temperature, humidity, wind speed, and any significant weather events.\n\n"
            f"- Current temperature: {current_temp:.2f} (feels like {feels_like_temp:.2f})\n"
            f"- Weather conditions: {current_conditions}\n"
            f"- Humidity: {current_humidity}%\n"
            # f"- Wind Speed: {current_wind_speed} m/s from {current_wind_deg} degrees\n"
            # f"- Visibility: {current_visibility} meters\n"
            # f"- Pressure: {current_pressure} hPa\n"
            # f"- UV Index: {current_uvi}\n\n"
            # f"**Hourly Forecast (next 3 hours):**\n"
            f"{hourly_forecast[0]}\n"
            f"{hourly_forecast[1]}\n"
            f"{hourly_forecast[2]}\n\n"
            f"- Daily Summary: {daily_summary}\n"
            f"- Daily Sunrise: {sunrise}, Sunset: {sunset}\n"
            f"- Daily Max Temperature: {max_temp:.2f}, Min Temperature: {min_temp:.2f}\n"
            f"- Daily Conditions: {daily_conditions}\n"
            f"- Daily Humidity: {daily_humidity}%\n"
            # f"- Wind: {daily_wind_speed} m/s from {daily_wind_deg} degrees\n"
            # f"- Rain: {daily_rain} mm\n"
            # f"- UV Index: {daily_uvi}\n\n"
            f"Make sure to use {Config().units} units for all temperatures and speeds.  Do not reference other units like miles or farenheight\n"
            "Keep response under 100 words"
        )

        return prompt
