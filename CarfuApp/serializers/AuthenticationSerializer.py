import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core import serializers as serialize
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.pagination import *

from CarfuApp.interfaces.LoginInterface import LoginInterface
from CarfuApp.models import UserModel


class LoginSerializer(serializers.ModelSerializer, PageNumberPagination):
    search_fields = ['username', 'email']

    class Meta:
        fields = ('username', 'email', 'is_staff', 'is_admin')

    def create(self, data):
        user = UserModel().create_user(username=data['username'], password=data['password'], email=data['email'])
        user.user_permissions.add(10, 11, 12, 13, 14, 15, 16)
        user.save()

        return user.values()

    def list_users(self):
        pass

    def update(self, instance, validated_data):
        instance.save()
        super(LoginSerializer, self).update(instance, validated_data)
        return json.loads(serialize.serialize('json', [instance])), None

    page_size = 30

    class Meta:
        fields = (
            'username',
            'password'
        )
        model = User

    def authenticate(self, request):
        data = request.data
        uname = data['username']
        password = data['password']
        result = dict()
        user = authenticate(username=uname, password=password)
        if user is not None and user.check_password(password):
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            result["token"] = token.key
            result["username"] = user.username
            result["user_id"] = user.pk
            return token

    @staticmethod
    def logout(request):
        logout(request)
        return True


class RegisterSerializer(serializers.ModelSerializer, PageNumberPagination):
    class Meta:
        model = User
        fields = (
            'email',
            'password',
            'username',
        )


class ReadUsers(serializers.ModelSerializer):
    class Meta:
        model = User
        read_only_fields = ['password']
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'is_staff',
            'is_active',
            'date_joined',
            'is_superuser',
            'last_login',
            'groups',
            'user_permissions'
        )

    @staticmethod
    def get_user():
        users = User.objects.all().defer("password")
        if users is not None:
            return users
        else:
            return None
