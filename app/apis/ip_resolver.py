import logging
import random
from typing import Callable, List

import requests

from app.models.ip_info import IPInfo

# Set up logging
logger = logging.getLogger(__name__)


class IPResolver:
    """
    A class to fetch the public IP address using various API endpoints.
    """

    def __init__(self, timeout: int = 5):
        self.api_functions: List[Callable[[], IPInfo]] = [
            self.get_ipinfo,
            self.get_ipwhois,
            self.get_ipapi,
        ]
        self.timeout = timeout

    def get_json_response(self, url: str) -> dict:
        """
        Make an HTTP GET request to the given URL and return the JSON response.

        Parameters:
        url (str): The URL to make the request to.

        Returns:
        dict: The JSON response.
        """
        try:
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error("Error fetching data from URL: %s", url, exc_info=True)
            raise e

    def get_ipinfo(self) -> IPInfo:
        """
        Get the public IP address and additional information using the ipinfo.io API.

        Returns:
        IPInfo: The public IP address and additional information.
        """
        url = "https://ipinfo.io/json"
        data = self.get_json_response(url)
        location = data.get("loc", "").split(",")
        latitude = float(location[0]) if location and len(location) > 1 else None
        longitude = float(location[1]) if location and len(location) > 1 else None
        return IPInfo(
            ip=data.get("ip"),
            hostname=data.get("hostname"),
            city=data.get("city"),
            region=data.get("region"),
            country=data.get("country"),
            latitude=latitude,
            longitude=longitude,
            timezone=data.get("timezone"),
        )

    def get_ipwhois(self) -> IPInfo:
        """
        Get the public IP address and additional information using the ipwho.is API.

        Returns:
        IPInfo: The public IP address and additional information.
        """
        url = "https://ipwho.is/"
        data = self.get_json_response(url)
        return IPInfo(
            ip=data.get("ip"),
            hostname=None,  # ipwho.is does not provide hostname
            city=data.get("city"),
            region=data.get("region"),
            country=data.get("country"),
            latitude=data.get("latitude"),
            longitude=data.get("longitude"),
            timezone=data.get("timezone", {}).get("id"),
        )

    def get_ipapi(self) -> IPInfo:
        """
        Get the public IP address and additional information using the ipapi.is API.

        Returns:
        IPInfo: The public IP address and additional information.
        """
        url = "https://api.ipapi.is/"
        data = self.get_json_response(url)
        location = data.get("location", {})
        return IPInfo(
            ip=data.get("ip"),
            hostname=None,  # ipapi.is does not provide hostname directly
            city=location.get("city"),
            region=location.get("state"),
            country=location.get("country"),
            latitude=location.get("latitude"),
            longitude=location.get("longitude"),
            timezone=location.get("timezone"),
        )

    def get_public_ip_info(self) -> IPInfo:
        """
        Get the public IP address and additional information by randomly selecting an API endpoint.

        Returns:
        IPInfo: The public IP address and additional information.
        """
        selected_function = random.choice(self.api_functions)
        return selected_function()


# if __name__ == "__main__":
#     try:
#         ip_resolver = IPResolver()
#         public_ip_info = ip_resolver.get_public_ip_info()
#         logger.info("Public IP information: %s", public_ip_info)
#     except Exception as e2:
#         logger.error("Failed to retrieve public IP information", exc_info=True)
