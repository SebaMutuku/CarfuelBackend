import uuid


class GenericResponse:
    @staticmethod
    def create_generic_response(status_code, request, message_code, message_description, error_code=None,
                                error_description=None,
                                additional_data=None, primary_data=None):
        message_id = str(uuid.uuid4())
        if request is not None and isinstance(request, dict):
            message_id = request.get("messageId")

        response = {
            "statusCode": status_code,
            "messageCode": message_code,
            "messageDescription": message_description,
            "messageId": message_id,
            "conversationID": str(uuid.uuid4()),
            "additionalData": additional_data if additional_data else [],
            "errorInfo": []
        }

        if primary_data is not None:
            response["primaryData"] = primary_data
        else:
            response["primaryData"] = None

        if error_code is not None and error_description is not None:
            response["errorInfo"].append({
                "errorCode": error_code,
                "errorDescription": error_description
            })
        return response
