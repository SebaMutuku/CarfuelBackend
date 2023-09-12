import json

from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core import serializers as serialize
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.pagination import PageNumberPagination

from CarfuApp.models import UserModel


class LoginSerializer(serializers.Serializer, PageNumberPagination):
    search_fields = ['username', 'email']
    model = get_user_model()

    class Meta:
        fields = ['username', 'email', 'is_staff', 'is_admin']
        extra_kwargs = {'username': {'validators': [UnicodeUsernameValidator()], }}

    @staticmethod
    def authenticate(request):
        data = request.data
        uname = data['username']
        password = data['password']
        user = authenticate(request, username=uname, password=password)
        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return token.key
        return None

    def create(self, data):
        user = UserModel().create_user(username=data['username'], password=data['password'], email=data['email'])
        user.user_permissions.add(10, 11, 12, 13, 14, 15, 16)
        user.save()
        user_data = dict()
        user_data["user_id"] = user.pk
        user_data["username"] = user.username
        user_data["email"] = user.email
        user_data["first_name"] = user.first_name
        user_data["last_name"] = user.last_name
        user_data["is_staff"] = user.is_staff
        user_data["is_active"] = user.is_active
        user_data["date_joined"] = user.date_joined
        return user_data

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
