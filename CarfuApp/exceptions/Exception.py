from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from rest_framework import status
from rest_framework.exceptions import ValidationError, APIException, AuthenticationFailed
from rest_framework.response import Response

from CarfuApp.utils.GenericResponse import GenericResponse


def exceptionhandler(exception, context):
    generic_response = GenericResponse()

    exception_map = {
        ValidationError: (status.HTTP_400_BAD_REQUEST, exception.args),
        APIException: (status.HTTP_500_INTERNAL_SERVER_ERROR, exception.args),
        IntegrityError: (status.HTTP_500_INTERNAL_SERVER_ERROR, exception.args),
        ObjectDoesNotExist: (status.HTTP_404_NOT_FOUND, exception.args),
        ValueError: (status.HTTP_500_INTERNAL_SERVER_ERROR, exception.args),
        AuthenticationFailed: (status.HTTP_401_UNAUTHORIZED, exception.args)
    }

    status_code, error_message = exception_map.get(type(exception),
                                                   (status.HTTP_500_INTERNAL_SERVER_ERROR, exception.args))
    response = Response(generic_response.create_generic_response(status_code, message_code=status_code,
                                                                 message_description=exception.args[0],
                                                                 message_id=context.get('messageID'),
                                                                 error_code=status_code,
                                                                 error_description=exception.args[0],
                                                                 additional_data=[],
                                                                 primary_data=None), status=status_code)

    return response
