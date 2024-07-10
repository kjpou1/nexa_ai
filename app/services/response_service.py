from flask_ask import question, statement


class ResponseService:
    @staticmethod
    def handle_response(payload):
        response_type = payload.get("type")
        response_text = payload.get("response")

        if response_type == "question":
            return question(response_text)
        elif response_type == "statement":
            return statement(response_text)
        else:
            # Default to statement if the type is not recognized
            return statement(response_text)
