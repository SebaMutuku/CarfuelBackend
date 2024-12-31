from datetime import datetime

from django import get_version
from django.db.models import Q
from django.shortcuts import render
from rest_framework import __version__ as drf_version
from rest_framework import status, views
from rest_framework.authentication import BasicAuthentication
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
                                                                      message_id=request.get("messageID"),
                                                                      message_description="Successfully logged in",
                                                                      error_description=None, error_code=None,
                                                                      additional_data=[], primary_data=data),
                            status=status.HTTP_200_OK)
        return Response({"payload": None, "message": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    def get(self, request, pk):
        user = models.AuthUser.objects.filter(pk=pk).values(
            'username', 'first_name', 'last_name', 'last_login',
            'is_active', 'date_joined', 'email', 'groups__permissions',
            'is_superuser', 'is_staff', 'user_permissions'
        ).first()
        if user:
            return Response({"message": "User found", "payload": user}, status=status.HTTP_200_OK)
        return Response({"message": "User not found", "payload": None}, status=status.HTTP_404_NOT_FOUND)

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
            return Response({"message": "User found"}, status=status.HTTP_200_OK)
        return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)


class Register(views.APIView):
    permission_classes = (AllowAny,)
    authentication_classes = [UserTokenAuthentication, BasicAuthentication]
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"user": serializer.data, "message": "Successfully created user"},
                            status=status.HTTP_201_CREATED)
        return Response({"message": "User with that username exists"}, status=status.HTTP_208_ALREADY_REPORTED)

    def get(self, request):
        pk = request.query_params.get("id")
        if pk:
            user = self.serializer_class.get_single_user(pk)
            if user:
                return Response({"data": user, "message": "success"}, status=status.HTTP_200_OK)
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        users = self.serializer_class.get_all_users()
        return Response({"data": users, "message": "success"}, status=status.HTTP_200_OK)
    def put(self,request):
        pass


class TaskView(views.APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (BasicAuthentication, UserTokenAuthentication)
    serializer_class = TaskSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Task saved successfully", "task": serializer.data}, status=status.HTTP_201_CREATED)

    def get(self, request):
        tasks = self.serializer_class.get_all_tasks()
        return Response({"message": "success", "payload": tasks}, status=status.HTTP_200_OK)

    def put(self, request, pk):
        task = Task.objects.get(pk=pk)
        serializer = self.serializer_class(task, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Task updated successfully", "task": serializer.data}, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        try:
            task = Task.objects.get(pk=pk)
            task.delete()
            return Response({"message": "Task deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Task.DoesNotExist:
            return Response({"message": f"Task with id {pk} not found"}, status=status.HTTP_404_NOT_FOUND)


class ActivityView(views.APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = [BasicAuthentication, UserTokenAuthentication]
    serializer_class = ActivitySerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Activity saved successfully", "activity": serializer.data},
                        status=status.HTTP_201_CREATED)

    def get(self, request):
        activities = self.serializer_class.get_all_task_activities()
        return Response({"message": "success", "payload": activities}, status=status.HTTP_200_OK)

    def put(self, request, pk):
        activity = TaskActivity.objects.get(pk=pk)
        serializer = self.serializer_class(activity, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Activity updated successfully", "activity": serializer.data},
                        status=status.HTTP_200_OK)

    def delete(self, request, pk):
        try:
            activity = TaskActivity.objects.get(pk=pk)
            activity.delete()
            return Response({"message": "Activity deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except TaskActivity.DoesNotExist:
            return Response({"message": f"Activity with id {pk} not found"}, status=status.HTTP_404_NOT_FOUND)


class HealthCheckView(views.APIView):
    def get(self, request):
        health_response = {
            "message": "all good now",
            "statusCode": status.HTTP_200_OK,
            "django_version": get_version(),
            "rest_framework_version": drf_version
        }
        return Response(health_response)
