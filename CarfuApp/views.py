from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import status, views
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.decorators import parser_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from CarfuApp.serializers import OrderSerializer, CarSerializer, AuthenticationSerializer
from . import models


class Login(views.APIView):
    permission_classes = (AllowAny,)
    serializer_class = AuthenticationSerializer.LoginSerializer
    parser_classes(JSONParser, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.authenticateuser(request)
            if user:
                return Response({"user": user, "message": "Successfully logged in"},
                                status=status.HTTP_200_OK)
        return Response({"user": None, "message": "Invalid Credentials"}, status.HTTP_401_UNAUTHORIZED)

    def get(self, request):
        username = request.data.get("username")
        user = User.objects.filter(username=username)
        if (user.username is not None and user.username == username) or (
                user.email is not None and user.email == username):
            return Response({"message": "User found"}, status=status.HTTP_200_OK)
        return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)


class Logout(views.APIView):
    permission_classes = ([IsAuthenticated])
    authentication_classes = ([BasicAuthentication, TokenAuthentication])
    parser_classes(JSONParser, )
    serializer_class = AuthenticationSerializer.LoginSerializer

    def post(self, request):
        username = request.data["username"]
        user = User.objects.filter(Q(username=username) | Q(email=username))
        if (user.username is not None and user.username == username) or (
                user.email is not None and user.email == username):
            return Response({"message": "User found"}, status=status.HTTP_200_OK)
        return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)


class GetSingleUser(views.APIView):
    permission_classes = ([AllowAny])
    authentication_classes = ([BasicAuthentication, TokenAuthentication])
    parser_classes(JSONParser, )
    serializer_class = AuthenticationSerializer.LoginSerializer

    def post(self, request):
        uname = request.data["username"]
        try:
            user = User.objects.get(Q(username=uname) | Q(email=uname))
            if (user.username is not None and user.username == uname) or (
                    user.email is not None and user.email == uname):
                return Response({"message": "User found", "status": status.HTTP_200_OK}, status=status.HTTP_200_OK)
            return Response({"message": "User not found", "status": status.HTTP_404_NOT_FOUND},
                            status=status.HTTP_404_NOT_FOUND)
        except BaseException as e:
            print(e)
            return Response({"message": "User not found", "status": status.HTTP_417_EXPECTATION_FAILED},
                            status=status.HTTP_417_EXPECTATION_FAILED)


class Register(views.APIView):
    permission_classes = (AllowAny,)
    querySet = User.objects.all()
    serializer_class = AuthenticationSerializer.RegisterSerializer
    parser_classes(JSONParser, )
    pagination_class = PageNumberPagination

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=False):
            user = serializer.adduser(request.data)
            if user:
                return Response(
                    {"user": user, "message": "Successfully created user", "responseCode": status.HTTP_202_ACCEPTED},
                    status=status.HTTP_202_ACCEPTED)
            else:
                return Response(
                    {"message": user, "responseCode": status.HTTP_208_ALREADY_REPORTED},
                    status=status.HTTP_208_ALREADY_REPORTED)

        else:
            print(serializer.errors)
            return Response(
                {"message": "user with that username exists", "responseCode": status.HTTP_208_ALREADY_REPORTED},
                status.HTTP_208_ALREADY_REPORTED)

    def get(self, request):
        user = User.objects.all().defer("password")
        serializer = AuthenticationSerializer.ReadUsers(user, many=True)
        response = {"message": "success", "responsePayload": serializer.data}
        return Response(response, status=status.HTTP_200_OK)


class Order(APIView):
    querySet = models.Orders.objects.all()
    renderer_classes = (JSONRenderer,)
    serializer_class = OrderSerializer.OrderSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (BasicAuthentication, TokenAuthentication)
    parser_classes(JSONParser, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            order = serializer.createOrder(request.data)
            if order:
                response = {"message": "Order Successful", "OrderDetails": serializer.data}
                return Response(response, status=status.HTTP_200_OK)
            response = {"message": "Order Failed", "OrderDetails": None}
            return Response(response, status=status.HTTP_417_EXPECTATION_FAILED)

        else:
            response = {"message": "Failed", "OrderDetails": None}
            return Response(response, status=status.HTTP_200_OK)

    def get(self, request):
        serializer = self.serializer_class
        return Response({"message": "success", "responsePayload": serializer.data})

    def update(self):
        pass


class CarsView(views.APIView):
    querySet = models.Cars.objects.all()
    renderer_classes = (JSONRenderer,)
    serializer_class = CarSerializer.CarSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = ([BasicAuthentication, TokenAuthentication])
    parser_classes(MultiPartParser, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            created = serializer.saveCar(request.POST, request.FILES['image'])
            if created:
                response = {"message": "success"}
                return Response(response, status=status.HTTP_202_ACCEPTED)
        response = {"message": f"failed {serializer.error_messages}"}
        return Response(response, status=status.HTTP_417_EXPECTATION_FAILED)

    def get(self, request):
        serializer = CarSerializer.CarSerializer(self.serializer_class.get_all_cars(), many=True,
                                                 context={"request": request})
        response = {"message": "success", "responsePayload": serializer.data}
        return Response(response, status=status.HTTP_200_OK)


class CarBrandsView(views.APIView):
    renderer_classes = (JSONRenderer,)
    serializer_class = CarSerializer.CarSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    parser_classes(JSONParser, )

    def get(self, request):
        serializer = CarSerializer.CarSerializer(self.serializer_class.get_car_brands(), many=True)
        return Response({"message": "success", "responsePayload": serializer.data})
