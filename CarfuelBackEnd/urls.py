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
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls.static import static
from django.contrib import admin
from django.urls import re_path

from CarfuApp import views
from CarfuelBackEnd import settings

app_name = 'CarfuApp'

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^api/users/login', views.Login.as_view(), name='Login'),
    re_path('api/users/register', views.Register.as_view(), name='Register'),
    re_path('api/orders/createOrder', views.Order.as_view(), name='CreateOrder'),
    re_path('api/cars/allcars', views.CarsView.as_view(), name='cars'),
    re_path('api/cars/carbrands', views.CarBrandsView.as_view(), name='carbrands')
    # url('api/users/listusers', views.FetchUsers.as_view(), name='ListUsers'),
    # url('api/users/logout', views.Logout.as_view(), name='Logout'),
    # url('api/users/findbymail', views.FindUserByEmail.as_view(), name='FindUsersByEmail'),
    # url('api/users/googleApi', views.GoogleView.as_view(), name='GoogleApi'),
    # url('api/login', login_views.LoginView.as_view(), name='log'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
