import datetime

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone


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


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    phonenumber = models.CharField(max_length=20)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


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


class Orders(models.Model):
    orderid = models.AutoField(primary_key=True)
    ordernumber = models.CharField(max_length=50)
    ordertime = models.DateTimeField()
    customerid = models.OneToOneField(User, models.DO_NOTHING, db_column='pk')
    orderamount = models.FloatField()
    orderlocation = models.CharField(max_length=255)
    deliverytime = models.DateTimeField(blank=True, null=True)
    orderdetails = models.CharField(max_length=255, blank=True, null=True)
    orderstatus = models.CharField(max_length=50)
    deliveryagent = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'orders'


class Registeredvehicles(models.Model):
    carid = models.AutoField(primary_key=True)
    carname = models.CharField(max_length=50)
    carmodel = models.CharField(max_length=50)
    carcolor = models.CharField(max_length=50)
    carregnumber = models.CharField(max_length=50)
    registeredon = models.DateTimeField()
    userid = models.OneToOneField(User, models.DO_NOTHING, db_column='pk', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'registeredvehicles'


class Roles(models.Model):
    roleid = models.AutoField(primary_key=True)
    rolename = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = True
        db_table = 'roles'

    def __str__(self):
        return self.rolename


class Cars(models.Model):
    car_id = models.AutoField(primary_key=True)
    make = models.CharField(blank=False, max_length=1000)
    model = models.CharField(max_length=1000)
    color = models.CharField(max_length=20)
    yom = models.CharField(max_length=4)
    mileage = models.CharField(blank=True, max_length=1000)
    sell_status = models.BooleanField(default=False, null=False)
    price = models.CharField(blank=False, max_length=1000)
    imageUrl = models.ImageField(upload_to="images/%Y/%m/%d", blank=True,
                                 validators=[FileExtensionValidator(['png', 'jpg', 'gif', 'jpeg'])])
    car_description = models.CharField(blank=True, max_length=1000)
    saved_on = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'cars'

    def __str__(self):
        return self.make + self.model


class AddUsersIntoDb(BaseUserManager):
    @staticmethod
    def create_user(username, password, **kwargs):
        user = User.objects.create(username=username,
                                   is_superuser=False,
                                   is_staff=False,
                                   is_active=True,
                                   email=kwargs.get('email'))
        user.set_password(password)
        return user

    def create_superuser(self, password=None, username=None, phonenumber=None):
        user = self.create_user(username=username, password=password, email=phonenumber, is_active=True)
        user.is_staff = False
        user.is_admin = True
        user.is_superuser = True
        user.created_on = datetime.datetime.now(tz=timezone.utc)
        user.save()
        return user

    def create_normal_user(self, username=None, password=None, phonenumber=None):
        user = self.create_user(username=username, password=password, email=phonenumber)
        user.is_admin = False
        user.is_superuser = False
        user.is_staff = False
        user.save()
        return user

    def create_agent(self, username=None, password=None, phonenumber=None):
        user = self.create_user(username=username, password=password, email=phonenumber)
        user.is_staff = True
        user.is_admin = False
        user.save()
        return user
