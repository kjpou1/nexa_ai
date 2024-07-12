import logging
import os

from dotenv import load_dotenv

from app.apis.ip_resolver import IPResolver
from app.helpers.constants import DEFAULT_SERVER_HOST, DEFAULT_SERVER_PORT
from app.models import SingletonMeta


class Config(metaclass=SingletonMeta):

    _is_initialized = False

    def __init__(self):
        load_dotenv()  # Load environment variables from .env file
        # Prevent re-initialization
        if not self._is_initialized:
            self._server = None
            self._port = None
            self._intent = None
            # Initialize other configuration settings here
            self.logger = logging.getLogger(__name__)
            self._public_ip_info = None
            self._public_location = None
            self._units = Config.get("UNITS")
            self.load_location()

    @classmethod
    def initialize(cls):
        # Convenience method to explicitly initialize the Config
        # This method can be expanded to include more initialization parameters if needed
        cls()

    @staticmethod
    def get(key, default=None):
        return os.getenv(key, default)

    @property
    def server_host(self):
        return (
            self._server
            if self._server
            else self.get("SERVER_HOST", DEFAULT_SERVER_HOST)
        )

    @property
    def server_port(self):
        return (
            self._port
            if self._port
            else int(self.get("SERVER_PORT", DEFAULT_SERVER_PORT))
        )

    @property
    def intent(self):
        return self._intent if self._intent else self.get("INTENT", "GenericIntent")

    @property
    def public_ip_info(self):
        return self._public_ip_info

    @property
    def public_location(self):
        return self._public_location

    @property
    def units(self):
        return self._units

    def set_server_host(self, host):
        self._server = host

    def set_server_port(self, port):
        self._port = port

    def set_intent(self, intent):
        self._intent = intent

    def load_location(self):
        self.logger.info("Retieving public facing information.")
        self._public_ip_info = IPResolver().get_public_ip_info()
        self.logger.info(self._public_ip_info)
        self._public_location = f"{self._public_ip_info.city}, {self._public_ip_info.region}, {self._public_ip_info.country}"
