

import jwt
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from rest_framework import authentication, exceptions
from rest_framework import serializers
from rest_framework.pagination import *

from CarfuApp.models import Users, Roles, Orders, Registeredvehicles, AddUsersIntoDb
from CarfuelBackEnd import settings
from datetime import datetime,timedelta

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'email',
            'password'
        )
        model = Users

    @staticmethod
    def checkLoginCredentials(data):
        email = data['username']
        password = data['password']
        print("Invalid user", email, password)

        try:
            user = Users.objects.get(email__exact=email)
            encoded_password = password
            if user is not None:
                if user.is_active:
                    # if not user.logged_in != False:
                    if encoded_password == user.password:
                        secret_key = settings.SECRET_KEY
                        expirydate = datetime
                        claims = {
                            "id": user.user_id,
                            "subject": user.email,
                            "exp": expirydate,
                            "roleId": user.roleid
                        }
                        token = jwt.encode(claims, secret_key, algorithm='HS256')  # [1:].replace('\'', "")
                        token="oaoaoooaoaoo"
                        user.token = token
                        user.logged_in = True
                        user.last_login = datetime.today().strftime("%Y-%m-%d %H:%M")
                        user.save()
                    else:
                        raise serializers.ValidationError({"Message": "Invalid login Credentials", "token": ""})
                # else:
                #     raise serializers.ValidationError(
                #         {"Message": "User Already Logged in.Logout First", "token": ""})
                else:
                    raise serializers.ValidationError({"Message": "User is Inactive", "token": ""})

            else:
                raise serializers.ValidationError({"Message": "Invalid login Credentials", "token": ""})

        except ObjectDoesNotExist:
            token = None
        return token


class RegisterSerializer(serializers.ModelSerializer, PageNumberPagination):
    class Meta:
        model = Users
        fields = (
            'user_id',
            'email',
            'username',
            'roleid'
        )

    def addUser(self, data):
        if data['password'] is None:
            raise serializers.ValidationError({"Message": "Passwords do not match"})
        else:
            from django.core.validators import validate_email
            email = validate_email(data['email'])
            if email is False:
                raise serializers.ValidationError({"Message": "Please enter a valid email"})
            else:
                email_exist = Users.objects.filter(email=data['email'])

                if email_exist:
                    raise serializers.ValidationError(
                        {"Message": "User with email " + "[" + str(data['email']) + "]" + " already exists "})
                else:
                    password = data['password']
                    print("Encrypted password", password)
                    email = data.get('email')
                    username = data['username']
                    role = Roles.objects.get(roleid=data['roleId'])
                    print("RoleName is: ", role.rolename)

                    if role.rolename == "Admin":
                        user = AddUsersIntoDb().create_superuser(email=email, password=password, roleId=role,
                                                                 username=username)
                    elif role.rolename == "Agent":
                        user = AddUsersIntoDb().create_staffuser(email=email,
                                                                 password=password,
                                                                 username=username, roleId=role)
                    else:
                        user = AddUsersIntoDb().create_normal_user(email=email,
                                                                   password=password,
                                                                   username=username, roleId=role)
                    entityResponse = {'username': user.username,
                                      'user_id': user.user_id,
                                      'email': user.email,
                                      'roleid': role.rolename}
                    return entityResponse


class DecodeToken:
    @staticmethod
    def decodeToken(request):
        headers = authentication.get_authorization_header(request).split()
        if not headers or headers[0].lower() != b'token':
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
                    # print("user_id",user_id)
                    username = user_data['subject']
                    role = user_data['roleId']
                    # print("token name:...." + str(role))
                    db_user = UserModel.objects.get(email__iexact=username)
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
            except UserModel.DoesNotExist:
                loggedinuser = None
        return loggedinuser
