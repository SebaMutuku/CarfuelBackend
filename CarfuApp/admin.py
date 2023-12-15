from django.contrib import admin

from .models import Task, TaskActivity


# @admin.register(Roles)
# class RoleAdmin(admin.ModelAdmin):
# 	list_display = [f.name for f in Roles._meta.fields]


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Task._meta.fields]


@admin.register(TaskActivity)
class RegisteredVehicleAdmin(admin.ModelAdmin):
    list_display = [f.name for f in TaskActivity._meta.fields]
