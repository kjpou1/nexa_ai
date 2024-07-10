from dataclasses import dataclass, field
from typing import Optional
from urllib.parse import urlparse


@dataclass
class ModelConfig:
    """
    Data model for a single model configuration.

    Attributes:
        description (str): Description of the model configuration.
        base_url (str): Base URL for the API.
        api_key (str): API key for authentication.
        model (str): Model identifier.
        key (Optional[str]): Optional unique key for the model configuration.
    """

    description: str
    base_url: str
    api_key: str
    model: str
    key: Optional[str] = field(default=None)

    def __post_init__(self):
        self.base_url = self.validate_url(self.base_url)

    @staticmethod
    def validate_url(url: str) -> str:
        """Validate the URL format."""
        result = urlparse(url)
        if all([result.scheme, result.netloc]):
            return url
        else:
            raise ValueError(f"Invalid URL: {url}")
