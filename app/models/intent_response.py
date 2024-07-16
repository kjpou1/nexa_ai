from dataclasses import dataclass


@dataclass
class IntentResponseDetails:
    status: str
    data: str
    timestamp: str


@dataclass
class IntentResponse:
    request: str
    details: IntentResponseDetails
