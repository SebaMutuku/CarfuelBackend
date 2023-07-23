import json

import jwt
from deprecated import deprecated
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core import serializers as serialize
from django.http import HttpResponse, JsonResponse
from rest_framework import authentication, exceptions, serializers
from rest_framework.authtoken.models import Token
from rest_framework.pagination import *

from CarfuApp.models import AddUsersIntoDb, AuthUser
from CarfuelBackEnd import settings


class LoginSerializer(serializers.ModelSerializer, PageNumberPagination):
    search_fields = ['username', 'email']

    class Meta:
        fields = ('username', 'email', 'is_staff', 'is_admin')

    def create(self, data):
        user = AddUsersIntoDb().create_user(username=data['username'], password=data['password'], email=data['email'])
        user.user_permissions.add(10, 11, 12, 13, 14, 15, 16)
        user.save()
        # user_dict = list(user)
        # user_dict['first_name'] = user.first_name
        # user_dict['last_name'] = user.last_name
        # user_dict['username'] = user.username
        # user_dict['email'] = user.email
        # user_dict['is_superuser'] = user.is_superuser
        # user_dict['last_login'] = user.last_login
        # user_dict['is_active'] = user.is_active
        # user_dict['date_joined'] = user.date_joined
        # user_dict['user_permissions'] = user.user_permissions

        return user.values()

    def update(self, instance, validated_data):
        # instance.username = validated_data['username']
        # instance.email = validated_data['email']
        # instance.first_name = validated_data['first_name']
        # instance.last_name = validated_data['last_name']
        # instance.is_superuser = validated_data['is_superuser']
        # instance.is_active = validated_data['is_active']
        # instance.is_staff = validated_data['is_staff']
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
            return result

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


@deprecated(reason="Use Django Authentication instead")
class DecodeToken:
    @staticmethod
    def decode_token(request):
        headers = authentication.get_authorization_header(request).decode("ascii").split()
        if not headers or headers[0].lower() != 'token':
            loggedinuser = None
        elif len(headers) == 1:
            msg = 'Invalid token header. No credentials provided.'
            raise exceptions.AuthenticationFailed(msg)
        elif len(headers) > 2:
            msg = 'Invalid token header'
            raise exceptions.AuthenticationFailed(msg)
        else:
            try:
                token = headers[1]
                if token is None:
                    msg = 'Invalid token header'
                    raise exceptions.AuthenticationFailed(msg)
                else:
                    user_data = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                    user_id = user_data['id']
                    username = user_data['subject']
                    role = user_data['roleId']
                    db_user = User.objects.get(username=username)
                    db_token = db_user.token[1:].replace("\'", "")
                    passed_token = str(token)[2:].replace("\'", "")
                    if db_token == passed_token:
                        loggedinuser = dict()
                        loggedinuser['loggedinuser'] = loggedinuser
                        loggedinuser['roleId'] = role
                        loggedinuser['token'] = token
                    else:
                        loggedinuser = None
            except jwt.ExpiredSignatureError or jwt.DecodeError or jwt.InvalidTokenError:
                return HttpResponse({'Error': "Token is invalid"}, status="403")
            except AuthUser.DoesNotExist:
                loggedinuser = None
        return loggedinuser

    @classmethod
    def test_class(cls, name):
        return cls.test_class(name)
