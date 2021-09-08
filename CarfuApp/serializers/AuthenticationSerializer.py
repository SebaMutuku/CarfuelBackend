import jwt
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from rest_framework import authentication, exceptions
from rest_framework import serializers
from rest_framework.pagination import *

from CarfuApp.models import Users, Roles, Orders, Registeredvehicles, AddUsersIntoDb
from CarfuApp.utils import SMS
from CarfuelBackEnd import settings
from datetime import datetime, timedelta
import jwt
from rest_framework.response import Response


class LoginSerializer(serializers.ModelSerializer):
	class Meta:
		fields = (
			'username',
			'password'
		)
		model = Users
	
	def authenticateUser(self, data):
		username = data['username']
		password = data['password']
		token = None
		try:
			user = Users.objects.get(username=username)
			if user is not None:
				if user.is_active:
					# if not user.logged_in != False:
					if password == user.password:
						secret_key = settings.SECRET_KEY
						expirydate = datetime.now() + timedelta(days=1)
						claims = {
							"id": user.user_id,
							"subject": user.username,
							"exp": expirydate,
							"roleId": user.roleid.roleid
						}
						token = jwt.encode(claims, secret_key, algorithm='HS256')
						user.last_login = datetime.today().strftime("%Y-%m-%d %H:%M")
						user.token = token
						if (user.save()):
							return token
						return token
					else:
						raise serializers.ValidationError({"message": "Invalid Credentials", "token": ""})
				else:
					raise serializers.ValidationError({"message": "Inactive User", "token": ""})
			
			else:
				raise serializers.ValidationError({"message": "Invalid username", "token": ""})
		except ObjectDoesNotExist:
			return token


class RegisterSerializer(serializers.ModelSerializer, PageNumberPagination):
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
	
	def addUser(self, data):
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
				password = data['password']
				print("Encrypted password", password)
				phonenumber = data.get('phonenumber')
				username = data['username']
				role = Roles.objects.get(roleid=3)
				print("RoleName is: ", role.rolename)
				
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
		
		def get_user(self):
			users = Users.objects.values_list("user_id",
			                                  "username",
			                                  "phonenumber",
			                                  "created_on",
			                                  "last_login",
			                                  "is_admin",
			                                  "is_active",
			                                  "roleid",
			                                  "is_agent")
			if user is not None:
				return user
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
					# print("user_id",user_id)
					username = user_data['subject']
					role = user_data['roleId']
					# print("token name:...." + str(role))
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
			except UserModel.DoesNotExist:
				loggedinuser = None
		return loggedinuser
