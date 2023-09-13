from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from rest_framework import status
from rest_framework.exceptions import ValidationError, APIException
from rest_framework.response import Response
from rest_framework.views import exception_handler


def exceptionhandler(exception, context):
    response = exception_handler(exception, context)
    print(f'Exception is--> {exception} and response ----> {response}')

    if response is not None:
        return response
    if isinstance(exception, ValidationError):
        return Response({'message': exception.args, "status": status.HTTP_500_INTERNAL_SERVER_ERROR},
                        status=status.HTTP_400_BAD_REQUEST)
    if isinstance(exception, APIException):
        return Response({'message': exception.args, "status": status.HTTP_500_INTERNAL_SERVER_ERROR},
                        status=status.HTTP_400_BAD_REQUEST)
    if isinstance(exception, IntegrityError):
        return Response({'message': exception.args, "status": status.HTTP_500_INTERNAL_SERVER_ERROR},
                        status=status.HTTP_400_BAD_REQUEST)
    if isinstance(exception, ObjectDoesNotExist):
        return Response({'message': exception.args, "status": status.HTTP_404_NOT_FOUND},
                        status=status.HTTP_400_BAD_REQUEST)

    return Response({'message': f'An error occurred while processing your request. {exception.args}',
                     "status": status.HTTP_500_INTERNAL_SERVER_ERROR}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
