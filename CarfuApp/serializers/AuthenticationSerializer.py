import jwt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from rest_framework import authentication, exceptions
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.pagination import *

from CarfuApp.models import Roles, AddUsersIntoDb, AuthUser
from CarfuelBackEnd import settings


class LoginSerializer(serializers.Serializer, PageNumberPagination):
    page_size = 30

    class Meta:
        fields = (
            'username',
            'password'
        )
        model = User

    # @staticmethod
    # def authenticateuser(data):
    #     uname = data['username']
    #     pword = data['password']
    #     user_response = dict()
    #     try:
    #         user = User.objects.get(username=uname)
    #         decryption_success = AESEncryption().decrypt_rsa(user.password, pword.strip())
    #         if user.username and decryption_success:
    #             secret_key = settings.SECRET_KEY
    #             expiry_date = datetime.datetime.now() + timedelta(days=1)
    #             token_claims = {"id": user.user_id,
    #                             "subject": user.username,
    #                             "role_id": user.roleid.roleid}
    #             token = jwt.encode(token_claims, secret_key, 'HS256')
    #             user.token = token
    #             user.last_login = datetime.datetime.now(tz=datetime.timezone.utc)
    #             user.save()
    #             user_response['token'] = token
    #             user_response['username'] = user.username
    #             user_response['role'] = user.roleid.roleid
    #             return user_response
    #         return user_response
    #     except User.DoesNotExist or Exception as e:
    #         print("Exception is ", e)
    #         return None

    @staticmethod
    def authenticateuser(request):
        data = request.data
        uname = data['username']
        pword = data['password']
        user_response = dict()
        try:
            user = authenticate(username=uname, password=pword)
            print(user.is_superuser, user.is_staff)
            if user is not None and user.check_password(pword):
                login(request, user)
                token, created = Token.objects.get_or_create(user=user)
                role_id = 1 if user.is_superuser else 2 if user.is_staff else 3
                user_response["token"] = token.key
                user_response["username"] = user.username
                user_response["role_id"] = role_id
                user_response["user_id"] = user.pk

                return user_response
            return user
        except (User.DoesNotExist or Exception) as e:
            print("Exception is ", e)
            return e

    @staticmethod
    def logout(request):
        try:
            logout(request)
            return True
        except Exception as e:
            print(e)
            return False


class RegisterSerializer(serializers.ModelSerializer, PageNumberPagination):
    class Meta:
        model = User
        fields = (
            'email',
            'password',
            'username',
        )

    @staticmethod
    def adduser(data):
        try:
            username = data['username']
            password = data['password']
            phonenumber = data['phonenumber']
            role = Roles.objects.get(roleid=3)
            if role.rolename == "Admin":
                user = AddUsersIntoDb().create_superuser(password=password,
                                                         username=username, phonenumber=phonenumber)
            elif role.rolename == "Agent":
                user = AddUsersIntoDb().create_staffuser(
                    password=password,
                    username=username, phonenumber=phonenumber)
            else:
                user = AddUsersIntoDb().create_normal_user(
                    password=password,
                    username=username, phonenumber=phonenumber)
            entity_response = {'username': user.username,
                               'user_id': user.pk,
                               'role': role.rolename}
            return entity_response
        except Exception as e:
            return ValidationError(e.args)


class ReadUsers(serializers.ModelSerializer):
    class Meta:
        model = User
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
