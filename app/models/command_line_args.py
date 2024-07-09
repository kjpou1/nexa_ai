from dataclasses import dataclass

from app.helpers.constants import DEFAULT_SERVER_HOST, DEFAULT_SERVER_PORT


@dataclass
class CommandLineArgs:
    server: str = DEFAULT_SERVER_HOST
    port: int = DEFAULT_SERVER_PORT
    intent: str = None
