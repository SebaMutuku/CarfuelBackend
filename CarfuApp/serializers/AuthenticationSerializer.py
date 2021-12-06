import datetime
from datetime import timedelta

import jwt
from django.http import HttpResponse
from rest_framework import authentication, exceptions
from rest_framework import serializers
from rest_framework.pagination import *

from CarfuApp.models import Users, Roles, AddUsersIntoDb, AuthUser
from CarfuApp.utils import SMS
from CarfuApp.utils.Security import AESEncryption
from CarfuelBackEnd import settings


class LoginSerializer(serializers.Serializer, PageNumberPagination):
    page_size = 30

    class Meta:
        fields = (
            'username',
            'password'
        )
        model = Users

    @staticmethod
    def authenticateuser(data):
        uname = data['username']
        pword = data['password']
        user_response = dict()
        try:
            user = Users.objects.get(username=uname, password=AESEncryption().encrypt_value(pword))
            if user.username and user.password:
                secret_key = settings.SECRET_KEY
                expiry_date = datetime.datetime.now() + timedelta(days=1)
                token_claims = {"id": user.user_id,
                                "subject": user.username,
                                "role_id": user.roleid.roleid}
                token = jwt.encode(token_claims, secret_key, 'HS256')
                user.token = token
                user.last_login = datetime.datetime.now(tz=datetime.timezone.utc)
                user.save()
                user_response['token'] = token
                user_response['username'] = user.username
                user_response['role'] = user.roleid.roleid
                return user_response
            return user_response
        except Users.DoesNotExist or Exception as e:
            print("Exception is ", e)
            return None


class RegisterSerializer(serializers.ModelSerializer, PageNumberPagination):
    class Meta:
        model = Users
        fields = (
            'phonenumber',
            'password',
            'username',
        )

    @staticmethod
    def adduser(data):
        if data['password'] is None:
            raise serializers.ValidationError({"Message": "Passwords do not match"})
        else:
            username_exists = Users.objects.filter(username=data['username'])
            if username_exists:
                raise serializers.ValidationError(
                    {"Message": "User with username " + "[" + str(data['username']) + "]" + " already exists "})
            else:
                success = SMS.SendSMS.sendMessageBirdSMS(data=data)
                print("SMS response", success)
                password = AESEncryption().encrypt_value(data['password'])
                print("Encrypted password", password)
                phonenumber = data.get('phonenumber')
                username = data['username']
                role = Roles.objects.get(roleid=3)
                if role.rolename == "Admin":
                    user = AddUsersIntoDb().create_superuser(password=password, roleId=role,
                                                             username=username, phonenumber=phonenumber)
                elif role.rolename == "Agent":
                    user = AddUsersIntoDb().create_staffuser(
                        password=password,
                        username=username, roleId=role, phonenumber=phonenumber)
                else:
                    user = AddUsersIntoDb().create_normal_user(
                        password=password,
                        username=username, roleId=role, phonenumber=phonenumber)
                entityResponse = {'username': user.username,
                                  'user_id': user.user_id,
                                  'roleid': role.rolename}
                return entityResponse


class ReadUsers(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = (
            'user_id',
            'username',
            'phonenumber',
            'created_on',
            'last_login',
            'is_admin',
            'is_active',
            'roleid',
            'is_agent'
        )

    @staticmethod
    def get_user(self):
        users = Users.objects.all().defer("password", "token")
        if users is not None:
            return users
        else:
            return None


class DecodeToken:
    @staticmethod
    def decodeToken(request):
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
                    db_user = Users.objects.get(username=username)
                    db_token = db_user.token[1:].replace("\'", "")
                    passed_token = str(token)[2:].replace("\'", "")
                    if db_token == passed_token:
                        loggedinuser = dict()
                        loggedinuser['loggedinuser'] = loggedinuser
                        loggedinuser['roleId'] = role
                        loggedinuser['token'] = token
                    else:
                        loggedinuser = None
            except jwt.ExpiredSignature or jwt.DecodeError or jwt.InvalidTokenError:
                return HttpResponse({'Error': "Token is invalid"}, status="403")
            except AuthUser.DoesNotExist:
                loggedinuser = None
        return loggedinuser
