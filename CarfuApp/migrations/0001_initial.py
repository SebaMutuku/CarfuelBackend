# Generated by Django 4.2.5 on 2023-12-18 18:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="AuthGroup",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=150, unique=True)),
            ],
            options={
                "db_table": "auth_group",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="AuthGroupPermissions",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
            ],
            options={
                "db_table": "auth_group_permissions",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="AuthPermission",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("codename", models.CharField(max_length=100)),
            ],
            options={
                "db_table": "auth_permission",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="AuthtokenToken",
            fields=[
                (
                    "key",
                    models.CharField(max_length=40, primary_key=True, serialize=False),
                ),
                ("created", models.DateTimeField()),
            ],
            options={
                "db_table": "authtoken_token",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="AuthUserGroups",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
            ],
            options={
                "db_table": "auth_user_groups",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="AuthUserUserPermissions",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
            ],
            options={
                "db_table": "auth_user_user_permissions",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="DjangoAdminLog",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("action_time", models.DateTimeField()),
                ("object_id", models.TextField(blank=True, null=True)),
                ("object_repr", models.CharField(max_length=200)),
                ("action_flag", models.SmallIntegerField()),
                ("change_message", models.TextField()),
            ],
            options={
                "db_table": "django_admin_log",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="DjangoContentType",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("app_label", models.CharField(max_length=100)),
                ("model", models.CharField(max_length=100)),
            ],
            options={
                "db_table": "django_content_type",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="DjangoMigrations",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("app", models.CharField(max_length=255)),
                ("name", models.CharField(max_length=255)),
                ("applied", models.DateTimeField()),
            ],
            options={
                "db_table": "django_migrations",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="DjangoSession",
            fields=[
                (
                    "session_key",
                    models.CharField(max_length=40, primary_key=True, serialize=False),
                ),
                ("session_data", models.TextField()),
                ("expire_date", models.DateTimeField()),
            ],
            options={
                "db_table": "django_session",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Oauth2ProviderAccesstoken",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("token", models.CharField(max_length=255, unique=True)),
                ("expires", models.DateTimeField()),
                ("scope", models.TextField()),
                ("created", models.DateTimeField()),
                ("updated", models.DateTimeField()),
            ],
            options={
                "db_table": "oauth2_provider_accesstoken",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Oauth2ProviderApplication",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("client_id", models.CharField(max_length=100, unique=True)),
                ("redirect_uris", models.TextField()),
                ("client_type", models.CharField(max_length=32)),
                ("authorization_grant_type", models.CharField(max_length=32)),
                ("client_secret", models.CharField(max_length=255)),
                ("name", models.CharField(max_length=255)),
                ("skip_authorization", models.BooleanField()),
                ("created", models.DateTimeField()),
                ("updated", models.DateTimeField()),
                ("algorithm", models.CharField(max_length=5)),
            ],
            options={
                "db_table": "oauth2_provider_application",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Oauth2ProviderGrant",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("code", models.CharField(max_length=255, unique=True)),
                ("expires", models.DateTimeField()),
                ("redirect_uri", models.TextField()),
                ("scope", models.TextField()),
                ("created", models.DateTimeField()),
                ("updated", models.DateTimeField()),
                ("code_challenge", models.CharField(max_length=128)),
                ("code_challenge_method", models.CharField(max_length=10)),
                ("nonce", models.CharField(max_length=255)),
                ("claims", models.TextField()),
            ],
            options={
                "db_table": "oauth2_provider_grant",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Oauth2ProviderIdtoken",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("jti", models.UUIDField(unique=True)),
                ("expires", models.DateTimeField()),
                ("scope", models.TextField()),
                ("created", models.DateTimeField()),
                ("updated", models.DateTimeField()),
            ],
            options={
                "db_table": "oauth2_provider_idtoken",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Oauth2ProviderRefreshtoken",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("token", models.CharField(max_length=255)),
                ("created", models.DateTimeField()),
                ("updated", models.DateTimeField()),
                ("revoked", models.DateTimeField(blank=True, null=True)),
            ],
            options={
                "db_table": "oauth2_provider_refreshtoken",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Task",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("expires_on", models.DateTimeField(auto_now=True)),
                (
                    "status",
                    models.CharField(
                        choices=[("pending", "Pending"), ("completed", "Completed")],
                        max_length=50,
                    ),
                ),
                ("title", models.CharField(blank=True, max_length=255, null=True)),
                ("description", models.CharField(max_length=10000)),
            ],
            options={
                "db_table": "CarfuApp_task",
                "managed": True,
            },
        ),
        migrations.CreateModel(
            name="TaskActivity",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("title", models.CharField(max_length=50)),
                ("description", models.CharField(max_length=10000)),
                ("expires_on", models.DateTimeField()),
                ("taskid", models.IntegerField()),
                (
                    "status",
                    models.CharField(
                        choices=[("pending", "Pending"), ("completed", "Completed")],
                        max_length=50,
                    ),
                ),
            ],
            options={
                "db_table": "CarfuApp_taskactivity",
                "managed": True,
            },
        ),
        migrations.CreateModel(
            name="AuthUser",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="first name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="last name"
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                ("username", models.CharField(max_length=255, unique=True)),
                ("email", models.EmailField(max_length=254, unique=True)),
                (
                    "phone_number",
                    models.CharField(blank=True, max_length=15, null=True),
                ),
                (
                    "gender",
                    models.CharField(
                        blank=True,
                        choices=[("Male", "F"), ("Female", "F"), ("Other", "O")],
                        max_length=20,
                        null=True,
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "db_table": "CarfuApp_authuser",
                "managed": True,
            },
        ),
        migrations.CreateModel(
            name="AuthUserToken",
            fields=[
                (
                    "key",
                    models.CharField(
                        max_length=40,
                        primary_key=True,
                        serialize=False,
                        verbose_name="Key",
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created"),
                ),
                ("expiry_date", models.DateTimeField(blank=True, null=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="auth_token",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="User",
                    ),
                ),
            ],
            options={
                "verbose_name": "Token",
                "verbose_name_plural": "Tokens",
                "abstract": False,
            },
        ),
    ]
