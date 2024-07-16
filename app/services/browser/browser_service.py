import logging
from datetime import datetime
from typing import Any, Dict, Optional

from app.config.config import Config

# Set up logging
logger = logging.getLogger(__name__)


class BrowserService:
    """
    A service class to handle weather forecast processing.
    """

    def __init__(self, api_key: Optional[str] = None):

        if api_key is None:
            api_key = Config.get("OPEN_WEATHER_MAP_KEY")

        self.config = Config()

    def web_search(self, search: str) -> str:
        """
        The user's non modified search contains the words 'web' or 'internet'

        Args:
            search (str): The non modified search string provided by the user where the search contains the words 'web' or 'internet' specifically.

        Returns:
            str: A comprehensive response generated by web or internet.
        """
        return "That is not supported for now."