from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from rest_framework import status
from rest_framework.exceptions import ValidationError, APIException, AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import exception_handler


def exceptionhandler(exception, context):
    response = exception_handler(exception, context)
    print(f'Error desc [ {exception}  \nError response ----> {response}')

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

    return Response(
        {'message': f'An error occurred while processing your request. {error_message}', 'status': status_code},
        status=status_code)
