import json
from datetime import timedelta
from typing import Optional, List

from django.contrib.auth import authenticate, login, logout
from django.core import serializers as serialize
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from CarfuApp.models.models import UserManager, AuthUser, AuthUserToken, DjangoSession


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255, write_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)
    expiry_date = serializers.DateTimeField(read_only=True)
    email = serializers.EmailField(read_only=True)
    user_id = serializers.IntegerField(read_only=True)

    def validate(self, data):
        user = authenticate(username=data.get("username"), password=data.get("password"))
        if user is not None:
            login(self.context['request'], user)
            token, created = AuthUserToken.objects.get_or_create(user=user)
            token.expiry_date = token.created + timedelta(days=30)
            token.save()
            data.update({
                "token": token.key,
                "expiry_date": token.expiry_date,
                "email": user.email,
                "user_id": user.id,
                "user": str(user)
            })
            return data
        raise AuthenticationFailed("Invalid credentials.")

    @staticmethod
    def logout(request):
        logout(request)
        return True


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)

    class Meta:
        model = AuthUser
        fields = ('email', 'password', 'username', 'gender')

    def create(self, validated_data):
        return UserManager().create_standard_user(**validated_data)

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        return json.loads(serialize.serialize('json', [instance]))

    @staticmethod
    def get_single_user(pk: int) -> Optional[dict]:
        user = AuthUser.objects.filter(pk=pk).values(
            'username', 'first_name', 'last_name', 'last_login',
            'is_active', 'date_joined', 'email',
            'groups__permissions', 'is_superuser', 'is_staff',
            'user_permissions'
        ).first()
        return user or None

    @staticmethod
    def get_all_users() -> List[dict]:
        return list(AuthUser.objects.all().order_by("date_joined").values(
            'username', 'first_name', 'last_name', 'last_login',
            'is_active', 'date_joined', 'email',
            'groups__permissions', 'is_superuser', 'is_staff',
            'user_permissions'
        ))


class ReadUsers(serializers.ModelSerializer):
    class Meta:
        model = AuthUser
        read_only_fields = ['password']
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name',
            'is_staff', 'is_active', 'date_joined', 'is_superuser',
            'last_login', 'groups', 'user_permissions'
        )

    @staticmethod
    def get_users() -> List[AuthUser]:
        return list(AuthUser.objects.all().defer("password"))
