import datetime

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from rest_framework.authtoken.models import Token


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.OneToOneField(AuthGroup, models.DO_NOTHING)
    permission = models.OneToOneField('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.OneToOneField('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class UserManager(BaseUserManager):
    @staticmethod
    def create_user(username, password, email=None, **extra_fields):
        if not email:
            raise ValidationError('Invalid email address')
        user = AuthUser.objects.create(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.created_on = datetime.datetime.now(tz=timezone.get_current_timezone())
        return user

    def create_superuser(self, password=None, username=None, email=None, gender=None):
        user = self.create_user(username=username, password=password, email=self.normalize_email(email), gender=gender)
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.save()
        return user

    def create_standard_user(self, username=None, password=None, email=None, gender=None):
        user = self.create_user(username=username, password=password, email=email, gender=gender)
        user.is_admin = False
        user.is_superuser = False
        user.is_staff = False
        user.save()
        return user

    def create_agent(self, username=None, password=None, email=None, gender=None):
        user = self.create_user(username=username, password=password, email=email, gender=gender)
        user.is_staff = True
        user.is_admin = False
        user.save()
        return user


class AuthUser(AbstractUser):
    username = models.CharField(max_length=255, unique=True, null=False)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    gender = models.CharField(max_length=20, choices=[('Male', 'M'), ('Female', 'F'), ('Other', 'O')], blank=True,
                              null=True)
    objects = UserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'password', 'gender']

    class Meta:
        managed = True
        db_table = 'CarfuApp_authuser'

    def __str__(self):
        return self.username.format(self.email)


class AuthUserGroups(models.Model):
    user = models.OneToOneField(AuthUser, models.DO_NOTHING)
    group = models.OneToOneField(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.OneToOneField(AuthUser, models.DO_NOTHING)
    permission = models.OneToOneField(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class AuthtokenToken(models.Model):
    key = models.CharField(primary_key=True, max_length=40)
    created = models.DateTimeField()
    user = models.OneToOneField(AuthUser, models.DO_NOTHING, unique=True)

    class Meta:
        managed = False
        db_table = 'authtoken_token'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.OneToOneField('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.OneToOneField(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Oauth2ProviderAccesstoken(models.Model):
    id = models.BigAutoField(primary_key=True)
    token = models.CharField(unique=True, max_length=255)
    expires = models.DateTimeField()
    scope = models.TextField()
    application = models.OneToOneField('Oauth2ProviderApplication', models.DO_NOTHING, blank=True, null=True)
    user = models.OneToOneField(AuthUser, models.DO_NOTHING, blank=True, null=True)
    created = models.DateTimeField()
    updated = models.DateTimeField()
    source_refresh_token = models.OneToOneField('Oauth2ProviderRefreshtoken', models.DO_NOTHING, unique=True,
                                                blank=True,
                                                null=True)
    id_token = models.OneToOneField('Oauth2ProviderIdtoken', models.DO_NOTHING, unique=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'oauth2_provider_accesstoken'


class Oauth2ProviderApplication(models.Model):
    id = models.BigAutoField(primary_key=True)
    client_id = models.CharField(unique=True, max_length=100)
    redirect_uris = models.TextField()
    client_type = models.CharField(max_length=32)
    authorization_grant_type = models.CharField(max_length=32)
    client_secret = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    user = models.OneToOneField(AuthUser, models.DO_NOTHING, blank=True, null=True)
    skip_authorization = models.BooleanField()
    created = models.DateTimeField()
    updated = models.DateTimeField()
    algorithm = models.CharField(max_length=5)

    class Meta:
        managed = False
        db_table = 'oauth2_provider_application'


class Oauth2ProviderGrant(models.Model):
    id = models.BigAutoField(primary_key=True)
    code = models.CharField(unique=True, max_length=255)
    expires = models.DateTimeField()
    redirect_uri = models.TextField()
    scope = models.TextField()
    application = models.OneToOneField(Oauth2ProviderApplication, models.DO_NOTHING)
    user = models.OneToOneField(AuthUser, models.DO_NOTHING)
    created = models.DateTimeField()
    updated = models.DateTimeField()
    code_challenge = models.CharField(max_length=128)
    code_challenge_method = models.CharField(max_length=10)
    nonce = models.CharField(max_length=255)
    claims = models.TextField()

    class Meta:
        managed = False
        db_table = 'oauth2_provider_grant'


class Oauth2ProviderIdtoken(models.Model):
    id = models.BigAutoField(primary_key=True)
    jti = models.UUIDField(unique=True)
    expires = models.DateTimeField()
    scope = models.TextField()
    created = models.DateTimeField()
    updated = models.DateTimeField()
    application = models.OneToOneField(Oauth2ProviderApplication, models.DO_NOTHING, blank=True, null=True)
    user = models.OneToOneField(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'oauth2_provider_idtoken'


class Oauth2ProviderRefreshtoken(models.Model):
    id = models.BigAutoField(primary_key=True)
    token = models.CharField(max_length=255)
    access_token = models.OneToOneField(Oauth2ProviderAccesstoken, models.DO_NOTHING, unique=True, blank=True,
                                        null=True)
    application = models.OneToOneField(Oauth2ProviderApplication, models.DO_NOTHING)
    user = models.OneToOneField(AuthUser, models.DO_NOTHING)
    created = models.DateTimeField()
    updated = models.DateTimeField()
    revoked = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'oauth2_provider_refreshtoken'
        unique_together = (('token', 'revoked'),)


class Task(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    expires_on = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed')], max_length=50, null=True,
                              default='pending')
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=10000)

    def __str__(self):
        return self.title

    class Meta:
        managed = True
        db_table = 'CarfuApp_task'


class TaskActivity(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=10000)
    expires_on = models.DateTimeField()
    taskid = models.IntegerField(null=False, blank=False)
    status = models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed')], max_length=50,
                              default="pending")

    def __str__(self):
        return self.title

    class Meta:
        managed = True
        db_table = 'CarfuApp_taskactivity'


class AuthUserToken(Token):
    expiry_date = models.DateTimeField(null=True, blank=True)

    def token_is_expired(self):
        return self.expiry_date and timezone.now() > self.expiry_date
