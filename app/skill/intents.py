import json
import logging
from collections import defaultdict
from typing import Any, Dict, Optional

from flask import Blueprint
from flask_ask import Ask

from app.config.config import Config
from app.services.intents_service import IntentsService
from app.services.response_service import ResponseService

# Create a Blueprint named "api"
api_bp = Blueprint("api", __name__)

# Set up a logger for this module
logger = logging.getLogger(__name__)


# Since Alexa responses are usually short phrases,
# it’s convenient to put them in the same file.
# Flask-Ask has a Jinja template loader that loads multiple templates from a single YAML file.
# Templates are stored in a file called templates.yaml located in the application root.
def create_intent_handlers(app):
    config = Config()

    # Initialize Flask-Ask with the Flask app and blueprint
    ask = Ask(app, "/", api_bp)

    # Define the launch request handler
    @ask.launch
    def launch():
        response_payload = IntentsService.get_launch_message()
        return ResponseService.handle_response(response_payload)

    # Define the fallback intent handler
    @ask.intent("AMAZON.FallbackIntent")
    def fallback():
        response_payload = IntentsService.get_fallback_message()
        return ResponseService.handle_response(response_payload)

    # Define the custom intent handler dynamically
    @ask.intent(config.intent)
    def custom_intent(query):
        user_request = query
        payload = {"request": user_request}
        response_data = IntentsService.handle_request(payload)
        return ResponseService.handle_response(response_data)

    # Define a handler for another intent (e.g., GoodbyeIntent)
    @ask.intent("GoodbyeIntent")
    def goodbye():
        response_payload = IntentsService.get_goodbye_message()
        return ResponseService.handle_response(response_payload)

    # Define a handler for session ended request handler
    @ask.session_ended
    def session_ended():
        response_payload = IntentsService.get_session_ended_message()
        return ResponseService.handle_response(response_payload)

    # Define a handler for another custom intent (e.g., HelpIntent)
    @ask.intent("AMAZON.HelpIntent")
    def help_intent():
        response_payload = IntentsService.get_help_message()
        return ResponseService.handle_response(response_payload)

    # Define a handler for a custom intent (e.g., StopIntent)
    @ask.intent("AMAZON.StopIntent")
    def stop():
        response_payload = IntentsService.get_stop_message()
        return ResponseService.handle_response(response_payload)

    # Define a handler for a custom intent (e.g., CancelIntent)
    @ask.intent("AMAZON.CancelIntent")
    def cancel():
        response_payload = IntentsService.get_cancel_message()
        return ResponseService.handle_response(response_payload)

    # Define a handler for weather condition (e.g., CancelIntent)
    @ask.intent("AMAZON.SearchAction<object@WeatherForecast>")
    def weather_forecast():
        request = ask.request
        intent = request.intent
        payload = {"request": intent.slots}
        response_data = IntentsService.handle_weather_forecast(payload)
        return ResponseService.handle_response(response_data)

    @ask.intent("AMAZON.SearchAction<object@WeatherForecast[weatherCondition]>")
    def weather_condition():
        request = ask.request
        intent = request.intent
        payload = {"request": intent.slots}
        response_data = IntentsService.handle_weather_forecast(payload)
        return ResponseService.handle_response(response_data)

    @ask.intent("AMAZON.SearchAction<object@WeatherForecast[temperature]>")
    def weather_temperature():
        request = ask.request
        intent = request.intent
        payload = {"request": intent.slots}
        response_data = IntentsService.handle_weather_forecast(payload)
        return ResponseService.handle_response(response_data)

    @ask.intent("WeatherIntent")
    def weather_intent():
        request = ask.request
        intent = request.intent
        payload = {"request": intent.slots}
        response_data = IntentsService.handle_weather_forecast(payload)
        return ResponseService.handle_response(response_data)

    @ask.intent("COLTRANE_INTENT")
    def huh_intent():
        request = ask.request
        intent = request.intent
        payload = {"request": intent.slots}
        response_data = IntentsService.handle_weather_forecast(payload)
        return ResponseService.handle_response(response_data)


def register_skill_intents(app):
    # Register intent handlers with the given Flask app
    create_intent_handlers(app)
    # Put any other skill-related code here
