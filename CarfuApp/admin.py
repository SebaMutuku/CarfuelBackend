from django.contrib import admin
from django.apps import apps
from .models import Roles, Users, Orders, Registeredvehicles


@admin.register(Roles)
class RoleAdmin(admin.ModelAdmin):
	list_display = [f.name for f in Roles._meta.fields]


@admin.register(Users)
class UserAdmin(admin.ModelAdmin):
	list_display = [f.name for f in Users._meta.fields]


@admin.register(Orders)
class OrderAdmin(admin.ModelAdmin):
	list_display = [f.name for f in Orders._meta.fields]


@admin.register(Registeredvehicles)
class RegisteredVehicleAdmin(admin.ModelAdmin):
	list_display = [f.name for f in Registeredvehicles._meta.fields]
