# import requests


class IntentsService:
    WEBHOOK_URL = "https://yourwebhook.url/path"

    @staticmethod
    def handle_request(payload):
        response = "Holy crap on a cracker"  # requests.post(IntentsService.WEBHOOK_URL, json=payload)
        # response.raise_for_status()  # Raise an error on bad status
        # response_json = response.json()
        return {"type": "statement", "response": response}

    @staticmethod
    def get_launch_message():
        return {
            "type": "question",
            "response": "Welcome to Nexa! How can I assist you today?",
        }

    @staticmethod
    def get_fallback_message():
        return {
            "type": "question",
            "response": "Sorry, I didn't get that. Can you please repeat?",
        }

    @staticmethod
    def get_goodbye_message():
        return {"type": "statement", "response": "Goodbye! Have a great day!"}

    @staticmethod
    def get_help_message():
        return {
            "type": "question",
            "response": "You can ask me to do various tasks like setting reminders, providing weather updates, and more. How can I help you?",
        }

    @staticmethod
    def get_stop_message():
        return {"type": "statement", "response": "Stopping now. Have a great day!"}

    @staticmethod
    def get_cancel_message():
        return {
            "type": "statement",
            "response": "Canceling your request. Have a great day!",
        }

    @staticmethod
    def get_session_ended_message():
        return {
            "type": "statement",
            "response": "We are done here. Have a great day!",
        }
