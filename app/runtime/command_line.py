import argparse

from app.helpers.constants import DEFAULT_SERVER_HOST, DEFAULT_SERVER_PORT
from app.models import CommandLineArgs


class CommandLine:
    @staticmethod
    def parse_arguments() -> CommandLineArgs:
        parser = argparse.ArgumentParser(
            description="Run the application with specified arguments."
        )

        parser.add_argument(
            "--server", "-s", type=str, default=DEFAULT_SERVER_HOST, help="Server host"
        )
        parser.add_argument(
            "--port", "-p", type=int, default=DEFAULT_SERVER_PORT, help="Server port"
        )
        parser.add_argument(
            "--intent",
            type=str,
            default="MyCustomIntent",
            help="Name of the custom intent",
        )

        args = parser.parse_args()

        return CommandLineArgs(server=args.server, port=args.port, intent=args.intent)
