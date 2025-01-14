from datetime import datetime

from django import get_version
from django.contrib.auth import logout
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.shortcuts import render
from rest_framework import __version__ as drf_version, serializers
from rest_framework import status, views
from rest_framework.authentication import BasicAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from CarfuApp.serializers import LoginSerializer, RegisterSerializer
from . import models
from .authentication.Authentication import UserTokenAuthentication
from .models import Task, TaskActivity
from .serializers import TaskSerializer, ActivitySerializer
from .utils.GenericResponse import GenericResponse


def index(request):
    now = datetime.now()
    return render(request, 'home.html', {'now': now})


class Login(views.APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=False):
            data = {
                'username': serializer.validated_data['user'],
                'user_id': serializer.validated_data['user_id'],
                'email': serializer.validated_data['email'],
                'token': serializer.validated_data['token'],
                'expiry_date': serializer.validated_data['expiry_date'],
            }
            return Response(GenericResponse().create_generic_response(status_code=status.HTTP_200_OK,
                                                                      message_code=status.HTTP_200_OK,
                                                                      request=request.data,
                                                                      message_description="Successfully logged in",
                                                                      error_description=None, error_code=None,
                                                                      additional_data=[], primary_data=data),
                            status=status.HTTP_200_OK)
        return AuthenticationFailed("Invalid login credentials")

    def get(self, request, pk):
        user = models.AuthUser.objects.filter(pk=pk).values(
            'username', 'first_name', 'last_name', 'last_login',
            'is_active', 'date_joined', 'email', 'groups__permissions',
            'is_superuser', 'is_staff', 'user_permissions'
        ).first()
        if user:
            return Response(GenericResponse().create_generic_response(status_code=status.HTTP_200_OK,
                                                                      message_code=status.HTTP_200_OK,
                                                                      request=request,
                                                                      message_description="Success",
                                                                      error_description=None, error_code=None,
                                                                      additional_data=[], primary_data=user),
                            status=status.HTTP_200_OK)
        return ObjectDoesNotExist("User not found")

    def put(self, request, pk):
        instance = models.AuthUser.objects.get(pk=pk)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.update(instance, validated_data=request.data)
            return Response({"message": "User updated successfully", "data": user}, status=status.HTTP_200_OK)
        return Response({"message": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)


class Logout(views.APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [BasicAuthentication, UserTokenAuthentication]

    def post(self, request):
        username = request.data.get("username")
        user = models.AuthUser.objects.filter(Q(username=username) | Q(email=username)).first()
        if user:
            logout(request)
            return Response({"message": "User found"}, status=status.HTTP_200_OK)
        return ObjectDoesNotExist("User does not exits or not logged in")


class Register(views.APIView):
    permission_classes = (AllowAny,)
    authentication_classes = [UserTokenAuthentication, BasicAuthentication]
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(GenericResponse().create_generic_response(status_code=status.HTTP_201_CREATED,
                                                                      message_code=status.HTTP_201_CREATED,
                                                                      request=request,
                                                                      message_description="Successfully create user",
                                                                      error_description=None, error_code=None,
                                                                      additional_data=[], primary_data=serializer.data),
                            status=status.HTTP_201_CREATED)
        return serializers.ValidationError(f"Failed to add the user with errors {serializer.errors}")

    def get(self, request):
        pk = request.query_params.get("id")
        if pk:
            user = self.serializer_class.get_single_user(pk)
            if user:
                return Response({"data": user, "message": "success"}, status=status.HTTP_200_OK)
            raise ObjectDoesNotExist(f"User with ID {pk} not found")

        users = self.serializer_class.get_all_users()
        return Response(GenericResponse().create_generic_response(status_code=status.HTTP_200_OK,
                                                                  message_code=status.HTTP_200_OK,
                                                                  request=request,
                                                                  message_description="Success",
                                                                  error_description=None, error_code=None,
                                                                  additional_data=[], primary_data=users),
                        status=status.HTTP_200_OK)

    def put(self, request):
        pass


class TaskView(views.APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (BasicAuthentication, UserTokenAuthentication)
    serializer_class = TaskSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(GenericResponse().create_generic_response(status_code=status.HTTP_201_CREATED,
                                                                  message_code=status.HTTP_201_CREATED,
                                                                  request=request,
                                                                  message_description="Task saved successfully",
                                                                  error_description=None, error_code=None,
                                                                  additional_data=[], primary_data=serializer.data),
                        status=status.HTTP_201_CREATED)

    def get(self, request):
        tasks = self.serializer_class.get_all_tasks()
        return Response(GenericResponse().create_generic_response(status_code=status.HTTP_200_OK,
                                                                  message_code=status.HTTP_200_OK,
                                                                  request=request,
                                                                  message_description="Success",
                                                                  error_description=None, error_code=None,
                                                                  additional_data=[], primary_data=tasks),
                        status=status.HTTP_200_OK)

    def put(self, request, pk):
        task = Task.objects.get(pk=pk)
        serializer = self.serializer_class(task, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(GenericResponse().create_generic_response(status_code=status.HTTP_200_OK,
                                                                  message_code=status.HTTP_200_OK,
                                                                  request=request,
                                                                  message_description="Success",
                                                                  error_description=None, error_code=None,
                                                                  additional_data=[], primary_data=serializer.data),
                        status=status.HTTP_200_OK)

    def delete(self, request, pk):
        try:
            task = Task.objects.get(pk=pk)
            task.delete()
            return Response(GenericResponse().create_generic_response(status_code=status.HTTP_200_OK,
                                                                      message_code=status.HTTP_200_OK,
                                                                      request=request,
                                                                      message_description="Task deleted successfully",
                                                                      error_description=None, error_code=None,
                                                                      additional_data=[], primary_data=None),
                            status=status.HTTP_200_OK)
        except Task.DoesNotExist:
            raise ObjectDoesNotExist(f"Task with that {pk} not found")


class ActivityView(views.APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = [BasicAuthentication, UserTokenAuthentication]
    serializer_class = ActivitySerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(GenericResponse().create_generic_response(status_code=status.HTTP_200_OK,
                                                                  message_code=status.HTTP_200_OK,
                                                                  request=request,
                                                                  message_description="Activity saved successfully",
                                                                  error_description=None, error_code=None,
                                                                  additional_data=[], primary_data=serializer.data),
                        status=status.HTTP_201_CREATED)

    def get(self, request):
        activities = self.serializer_class.get_all_task_activities()
        return Response(GenericResponse().create_generic_response(status_code=status.HTTP_200_OK,
                                                                  message_code=status.HTTP_200_OK,
                                                                  request=request,
                                                                  message_description="Success",
                                                                  error_description=None, error_code=None,
                                                                  additional_data=[], primary_data=activities),
                        status=status.HTTP_200_OK)

    def put(self, request, pk):
        activity = TaskActivity.objects.get(pk=pk)
        serializer = self.serializer_class(activity, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(GenericResponse().create_generic_response(status_code=status.HTTP_200_OK,
                                                                  message_code=status.HTTP_200_OK,
                                                                  request=request,
                                                                  message_description="Activity updated successfully",
                                                                  error_description=None, error_code=None,
                                                                  additional_data=[], primary_data=serializer.data),
                        status=status.HTTP_200_OK)

    def delete(self, request, pk):
        try:
            activity = TaskActivity.objects.get(pk=pk)
            activity.delete()
            return Response(GenericResponse().create_generic_response(status_code=status.HTTP_200_OK,
                                                                      message_code=status.HTTP_200_OK,
                                                                      request=request,
                                                                      message_description="Activity deleted successfully",
                                                                      error_description=None, error_code=None,
                                                                      additional_data=[], primary_data=activity),
                            status=status.HTTP_200_OK)
        except TaskActivity.DoesNotExist:
            raise ObjectDoesNotExist(f"Activity with id {pk} not found")


class HealthCheckView(views.APIView):
    def get(self, request):
        health_response = {
            "message": "all good now",
            "statusCode": status.HTTP_200_OK,
            "django_version": get_version(),
            "rest_framework_version": drf_version
        }
        return Response(health_response)
