import json
import random

from django.shortcuts import render
from rest_framework import status, views
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.decorators import parser_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from CarfuelBackEnd import settings
from . import models
from CarfuApp.serializers.AuthenticationSerializer import RegisterSerializer, DecodeToken, LoginSerializer
from CarfuApp.serializers.OrderSerializer import OrderSerializer
from .models import Orders
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from twilio.rest import Client
import messagebird
import requests


class Register(views.APIView):
    permission_classes = (AllowAny,)
    querySet = models.Users.objects.all()
    serializer_class = RegisterSerializer
    parser_classes(JSONParser, )
    pagination_class = PageNumberPagination

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.addUser(request.data)
            if user:
                return Response({"User": serializer.data, "Message": "Successfully created user ['{}']".format(
                    request.data.get('email'))},
                                status=status.HTTP_200_OK)
            else:
                return Response({serializer.error},
                                status=status.HTTP_401_UNAUTHORIZED)

        else:
            return Response(serializer.errors, status.HTTP_401_UNAUTHORIZED)


class Login(APIView):
    querySet = models.Roles.objects.all()
    renderer_classes = (JSONRenderer,)
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    parser_classes(JSONParser, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            token = serializer.authenticateUser(request.data)
            if token:
                response = {"message": "Successfully Logged In ", "token": token}
                return Response(response, status=status.HTTP_200_OK)
            else:
                response = {"message": serializer.errors, "token": ""}
                return Response(response, status=status.HTTP_200_OK)
        else:
            response = {"message": serializer.errors, "Token": ""}
            return Response(response, status=status.HTTP_401_UNAUTHORIZED)


class Order(APIView):
    querySet = models.Orders.objects.all()
    renderer_classes = (JSONRenderer,)
    serializer_class = OrderSerializer
    permission_classes = (AllowAny,)
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    parser_classes(JSONParser, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            order = serializer.createOrder(request.data)
            if order:
                response = {"message": "Order Successful", "OrderDetails": serializer.data}
                return Response(response, status=status.HTTP_200_OK)
            else:
                response = {"message": "Order Failed", "OrderDetails": None}
                return Response(response, status=status.HTTP_417_EXPECTATION_FAILED)

        else:
            response = {"message": "Failed", "OrderDetails": None}
            return Response(response, status=status.HTTP_200_OK)

    def get(self, request):
        model = Orders.objects.all()
        serializer = OrderSerializer(model, many=True)
        return Response({"message": "Success", "responsePayload": serializer.data})

    def update():
        pass







