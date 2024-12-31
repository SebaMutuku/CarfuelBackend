"""CarfuelBackEnd URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import to include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.urls import re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.urlpatterns import format_suffix_patterns

from CarfuApp import views
from CarfuelBackEnd import settings

app_name = 'CarfuApp'

schema_view = get_schema_view(
   openapi.Info(
      title="My API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@myapi.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)
urlpatterns = [
    path('', include('CarfuApp.urls')),
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^api/users/login', views.Login.as_view(), name='Login'),
    re_path('api/users/register', views.Register.as_view(), name='Register'),
    re_path('api/users/get', views.Register.as_view(), name='get_all_users'),
    re_path('api/users/logout', views.Logout.as_view(), name='logout'),
    re_path('api/tasks/create', views.TaskView.as_view(), name='create'),
    re_path(r'^api/tasks/update/(?P<pk>\d+)/$', views.TaskView.as_view(), name='task-update'),
    re_path('api/tasks/alltasks', views.TaskView.as_view(), name='all-tasks'),
    re_path(r'^api/tasks/delete/(?P<pk>\d+)/$', views.TaskView.as_view(), name='delete-task'),
    re_path('api/tasks/activity/create', views.ActivityView.as_view(), name='create'),
    re_path(r'^api/tasks/activity/update/(?P<pk>\d+)/$', views.ActivityView.as_view(), name='update-activity'),
    re_path(r'^api/tasks/activity/delete/(?P<pk>\d+)/$', views.ActivityView.as_view(), name='delete-activity'),
    re_path('api/tasks/activity/allactivities', views.ActivityView.as_view(), name='all-activities'),
    re_path('health', views.HealthCheckView.as_view(), name='health'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),
]
urlpatterns = format_suffix_patterns(urlpatterns)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
