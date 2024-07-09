import asyncio
import logging
import os

from flask import Flask
from flask_ask import Ask
from werkzeug.serving import run_simple

from app.config.config import Config
from app.models.command_line_args import CommandLineArgs
from app.skill.intents import api_bp, register_skill_intents


class TestingConfig(Config):
    DATABASE_URI = "sqlite:///:memory:"
    TESTING = True
    EXPLAIN_TEMPLATE_LOADING = True


class Host:
    """
    Host class to initialize and run the Flask application with command line arguments and configuration.

    Attributes:
    args (CommandLineArgs): Command line arguments passed to the script.
    config (Config): Configuration object based on command line arguments.
    logger (Logger): Logger instance for logging messages.
    app (Flask): Flask application instance.
    """

    def __init__(self, args: CommandLineArgs):
        """
        Initialize the Host class with command line arguments and configuration.

        Parameters:
        args (CommandLineArgs): Command line arguments passed to the script.
        """
        self.args = args

        self.config = Config()
        self.config.set_server_host(args.server)
        self.config.set_server_port(args.port)
        self.config.set_intent(args.intent)

        self.logger = logging.getLogger(__name__)
        # Initialize Flask app
        self.app = Flask(__name__)
        # # Register blueprints
        self.app.register_blueprint(api_bp)

        register_skill_intents(self.app)

    def run(self):
        # Method to perform the main logic: Start Flask server
        run_simple(
            self.args.server,
            self.args.port,
            self.app,
            use_debugger=self.config.get("DEBUG", False),
        )


# if __name__ == "__main__":
#     args = CommandLine.parse_arguments()
#     host = Host(args)
#     host.run()
