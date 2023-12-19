from datetime import datetime

from django import get_version
from django.db.models import Q
from django.http import HttpResponse
from rest_framework import __version__ as drf_version
from rest_framework import status, views
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import parser_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND
from rest_framework.views import APIView

from CarfuApp.serializers import LoginSerializer, RegisterSerializer
from . import models
from .authentication.Authentication import UserTokenAuthentication
from .serializers.TaskSerializer import TaskSerializer, ActivitySerializer


def index(request):
    now = datetime.now()
    html = f'''
    <html>
        <body>
            <h1>Welcome to Carfuel. If you are seeing this, your app works perfectly!</h1>
            <p>Deployment completed as at {now}.</p>
        </body>
    </html>
    '''
    return HttpResponse(html)


class Login(views.APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    parser_classes(JSONParser, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=False):
            user = serializer.validated_data['user']
            token = serializer.validated_data['token']
            token_expiry = serializer.validated_data['expiry_date']
            email = serializer.validated_data['email']
            user_id = serializer.validated_data['user_id']
            if user and token:
                data = {
                    'username': user,
                    'user_id': user_id,
                    'email': email,
                    'token': token,
                    'expiry_date': token_expiry,
                }
                return Response({"payload": data, "message": "Successfully logged in"},
                                status=status.HTTP_200_OK)
        return Response({"payload": None, "message": "Invalid Credentials"}, status.HTTP_401_UNAUTHORIZED)

    def get(self, request, pk):
        user = models.AuthUser.objects.filter(pk=pk).values('username', 'first_name', 'last_name', 'last_login',
                                                            'is_active',
                                                            'date_joined', 'email', 'groups__permissions',
                                                            'is_superuser',
                                                            'is_staff', 'user_permissions')
        if user:
            return Response({"message": "User found", "payload": user}, status=status.HTTP_200_OK)
        return Response({"message": "User not found", "payload": None}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk, format=None):
        instance = models.AuthUser.objects.get(pk=pk, format=format)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.update(instance, validated_data=request.data)
            return Response({"message": "User found", "data": user}, status=status.HTTP_200_OK)
        return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)


class Logout(views.APIView):
    permission_classes = ([IsAuthenticated])
    authentication_classes = ([BasicAuthentication, UserTokenAuthentication])
    parser_classes(JSONParser, )
    serializer_class = LoginSerializer

    def post(self, request):
        username = request.data["username"]
        user = models.AuthUser.objects.filter(Q(username=username) | Q(email=username))
        if (user.username is not None and user.username == username) or (
                user.email is not None and user.email == username):
            return Response({"message": "User found"}, status=status.HTTP_200_OK)
        return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)


class Register(views.APIView, PageNumberPagination):
    permission_classes = (AllowAny,)
    authentication_classes = ([UserTokenAuthentication, BasicAuthentication])
    querySet = models.AuthUser.objects.all()
    serializer_class = RegisterSerializer
    parser_classes(JSONParser, )
    pagination_class = PageNumberPagination
    page_size = 1000
    page_size_query_param = "page_size"
    max_page_size = 1000

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user = serializer.data
            if user:
                return Response(
                    {"user": user, "message": "Successfully created user", "responseCode": status.HTTP_201_CREATED},
                    status=status.HTTP_201_CREATED)
            else:
                return Response(
                    {"message": user, "responseCode": status.HTTP_208_ALREADY_REPORTED},
                    status=status.HTTP_208_ALREADY_REPORTED)

        return Response({"message": "user with that username exists", "responseCode": status.HTTP_208_ALREADY_REPORTED},
                        status.HTTP_208_ALREADY_REPORTED)

    def get(self, request):
        pk = request.query_params.get("id", None)
        if pk is not None:
            user = self.serializer_class.get_single_user(pk)
            if user is not None:
                return Response({"data": user, "message": "success", "responseCode": status.HTTP_302_FOUND},
                                status.HTTP_302_FOUND)
            return Response({"data": None, "message": "User not found", "responseCode": status.HTTP_404_NOT_FOUND},
                            status.HTTP_404_NOT_FOUND)
        users = self.serializer_class.get_all_users()
        if users is not None:
            return Response({"data": users, "message": "success", "responseCode": status.HTTP_302_FOUND},
                            status.HTTP_302_FOUND)
        return Response({"data": None, "message": "No data available", "responseCode": status.HTTP_204_NO_CONTENT},
                        status.HTTP_404_NOT_FOUND)


class TaskView(APIView):
    querySet = models.Task.objects.all()
    renderer_classes = (JSONRenderer,)
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (BasicAuthentication, UserTokenAuthentication)
    parser_classes(JSONParser, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            serializer.save()
            task = serializer.data
            if task:
                response = {"message": "Task saved successfully", "task": serializer.data}
                return Response(response, status=status.HTTP_201_CREATED)
            response = {"message": "Failed to save your Task", "task": None}
            return Response(response, status=status.HTTP_417_EXPECTATION_FAILED)

        else:
            response = {"message": "Failed", "task": None}
            return Response(response, status=status.HTTP_200_OK)

    def get(self, request):
        data = self.serializer_class.get_all_tasks()
        if len(data) != 0:
            response = {"message": "success", "payload": data}
            return Response(response, status=status.HTTP_200_OK)
        return Response({"message": "No tasks available", "payload": []}, status=HTTP_404_NOT_FOUND)

    def put(self, request):
        serializer = self.serializer_class(data=request.data, )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            task = serializer.data
            if task:
                response = {"message": "Task saved successfully", "task": serializer.data}
                return Response(response, status=status.HTTP_200_OK)
            response = {"message": "Failed to save your Task", "task": None}
            return Response(response, status=status.HTTP_417_EXPECTATION_FAILED)


class ActivityView(views.APIView):
    querySet = models.TaskActivity.objects.all()
    renderer_classes = (JSONRenderer,)
    serializer_class = ActivitySerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = ([BasicAuthentication, UserTokenAuthentication])
    parser_classes(MultiPartParser, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            serializer.save()
            activity_data = serializer.data
            if activity_data:
                response = {"message": "Saved successfully", "activity": serializer.data}
                return Response(response, status=status.HTTP_201_CREATED)
        response = {"message": f"Failed {serializer.error_messages}"}
        return Response(response, status=status.HTTP_417_EXPECTATION_FAILED)

    def get(self, request):
        serializer = self.serializer_class.get_all_task_activities()
        if len(serializer.data) != 0:
            response = {"message": "success", "payload": serializer.data}
            return Response(response, status=status.HTTP_200_OK)
        return Response({"message": "No activities available", "payload": []}, status=HTTP_404_NOT_FOUND)

    def put(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            task = serializer.data
            if task:
                response = {"message": "Saved successfully", "taskActivity": serializer.data}
                return Response(response, status=status.HTTP_200_OK)
            response = {"message": "Failed to save your Task", "taskActivity": None}
            return Response(response, status=status.HTTP_417_EXPECTATION_FAILED)


class HealthCheckView(views.APIView):
    renderer_classes = (JSONRenderer,)

    def get(self, request, *args, **kwargs):
        health_response = {
            "message": "all good now",
            "statusCode": status.HTTP_200_OK,
            "django_version": get_version(),
            "rest_framework_version": drf_version
        }
        return Response(health_response)
