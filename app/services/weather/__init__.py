# app/services/weather/__init__.py
# Import and expose from subpackages if needed
from .weather_service import WeatherService

# Optional, for explicit API exposure
__all__ = ["WeatherService"]
