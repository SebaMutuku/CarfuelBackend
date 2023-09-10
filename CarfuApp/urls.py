from django.urls import path

from CarfuApp.views import index

urlpatterns = [
    path('', index),
]
