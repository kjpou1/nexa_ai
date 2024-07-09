import logging

from flask import Blueprint, render_template
from flask_ask import Ask, question, statement

from app.config.config import Config

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
        # Render the welcome_text template from templates.yaml
        welcome_text = render_template("welcome_text")
        return question(welcome_text)

    # Define the fallback intent handler
    @ask.intent("AMAZON.FallbackIntent")
    def fallback():
        # Render the ask_name_reprompt template from templates.yaml
        reprompt_text = render_template("ask_name_reprompt")
        return question(reprompt_text)

    # # Define the custom intent handler dynamically
    @ask.intent(config.intent)
    def custom_intent(firstname):
        if firstname is None:
            # No name given, prompt user to provide their name
            ask_name_text = render_template("ask_name")
            return question(ask_name_text)
        # Render the hello template with the provided firstname
        response_text = render_template("hello", firstname=firstname)
        return statement(response_text).simple_card("Hello", response_text)

    # Define a handler for another intent (e.g., GoodbyeIntent)
    @ask.intent("GoodbyeIntent")
    def goodbye():
        # Placeholder for GoodbyeIntent logic
        goodbye_text = render_template("goodbye")
        return statement(goodbye_text)

    # Define a handler for another custom intent (e.g., HelpIntent)
    @ask.intent("AMAZON.HelpIntent")
    def help():
        # Placeholder for HelpIntent logic
        help_text = render_template("help")
        return question(help_text)

    # Define a handler for a custom intent (e.g., StopIntent)
    @ask.intent("AMAZON.StopIntent")
    def stop():
        # Placeholder for StopIntent logic
        stop_text = render_template("stop")
        return statement(stop_text)

    # Define a handler for a custom intent (e.g., CancelIntent)
    @ask.intent("AMAZON.CancelIntent")
    def cancel():
        # Placeholder for CancelIntent logic
        cancel_text = render_template("cancel")
        return statement(cancel_text)


def register_skill_intents(app):
    # Register intent handlers with the given Flask app
    create_intent_handlers(app)
    # Put any other skill-related code here
