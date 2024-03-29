import json
from datetime import timedelta
from typing import Optional

from django.contrib.auth import authenticate, login, logout
from django.core import serializers as serialize
from django.http import JsonResponse
from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination

from CarfuApp.models.models import UserManager, AuthUser, AuthUserToken


class LoginSerializer(serializers.Serializer, PageNumberPagination):
    search_fields = ['username', 'email']
    password = serializers.CharField(max_length=128, write_only=True)
    username = serializers.CharField(max_length=255, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")
        user = authenticate(username=username, password=password)
        validated_user = AuthUser.objects.get(username=username)
        data["token"] = None
        data["expiry_date"] = None
        data["user"] = None
        if user is not None and validated_user:
            login(self.context['request'], user=user)
            token, created = AuthUserToken.objects.get_or_create(user=user)
            token.expiry_date = token.created + timedelta(days=30)
            token.save()
            data["user"] = str(user)
            data["token"] = str(token.key)
            data["expiry_date"] = token.expiry_date
            data["email"] = str(validated_user.email)
            data["user_id"] = validated_user.id
            return data
        return data

    class Meta:
        fields = (
            'username',
            'password'
        )
        model = AuthUser

    @staticmethod
    def logout(request):
        logout(request)
        return True


class RegisterSerializer(serializers.ModelSerializer, PageNumberPagination):
    password = serializers.CharField(max_length=128, min_length=8, write_only=True, )

    class Meta:
        model = AuthUser
        fields = ('email', 'password', 'username', 'gender')

    def create(self, validated_data):
        return UserManager().create_standard_user(username=validated_data['username'],
                                                  password=validated_data['password'],
                                                  email=validated_data['email'],
                                                  gender=validated_data['gender'])

    def update(self, instance, validated_data):
        super(RegisterSerializer, self).update(instance, validated_data)
        return json.loads(serialize.serialize('json', [instance])), None

    @staticmethod
    def get_single_user(pk: int) -> Optional[JsonResponse]:
        return AuthUser.objects.filter(pk=pk).values('username', 'first_name', 'last_name', 'last_login', 'is_active',
                                                     'date_joined', 'email', 'groups__permissions', 'is_superuser',
                                                     'is_staff', 'user_permissions') or None

    @staticmethod
    def get_all_users() -> tuple[list[AuthUser], None]:
        return AuthUser.objects.all().order_by("date_joined").values('username', 'first_name',
                                                                     'last_name', 'last_login',
                                                                     'is_active',
                                                                     'date_joined', 'email',
                                                                     'groups__permissions',
                                                                     'is_superuser',
                                                                     'is_staff', 'user_permissions'), None


class ReadUsers(serializers.ModelSerializer):
    class Meta:
        model = AuthUser
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
        users = AuthUser.objects.all().defer("password")
        if users is not None:
            return users
        else:
            return None
