import json

from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.models import User
from django.core import serializers as serialize
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.pagination import PageNumberPagination

from CarfuApp.models import UserModel


class LoginSerializer(serializers.Serializer, PageNumberPagination):
    search_fields = ['username', 'email']
    password = serializers.CharField(max_length=128, write_only=True)
    username = serializers.CharField(max_length=255, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        user = authenticate(username=data.get("username"), password=data.get("password", None))
        if user is not None:
            login(self.context['request'], user=user)
            token, created = Token.objects.get_or_create(user=user)
            return {'token': token or None}
        return {"token": None}

    def list_users(self):
        pass

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
    password = serializers.CharField(max_length=128, min_length=8, write_only=True, )

    class Meta:
        model = User
        fields = ('email', 'password', 'username',)

    def create(self, validated_data):
        return UserModel().create_standard_user(username=validated_data['username'],
                                                password=validated_data['password'],
                                                email=validated_data['email'])

    def update(self, instance, validated_data):
        instance.save()
        super(RegisterSerializer, self).update(instance, validated_data)
        return json.loads(serialize.serialize('json', [instance])), None


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
