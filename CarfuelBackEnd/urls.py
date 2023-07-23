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
from django.urls import re_path,path

from CarfuApp import views
from CarfuelBackEnd import settings

app_name = 'CarfuApp'

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^api/users/login', views.Login.as_view(), name='Login'),
    re_path('api/users/<int:pk>', views.Login.as_view()),
    re_path('api/users/register', views.Register.as_view(), name='Register'),
    path('api/users/<int:pk>', views.Login.as_view()),
    re_path('api/users/logout', views.Logout.as_view(), name='logout'),
    re_path('api/users/getUser', views.GetSingleUser.as_view(), name='Viewuser'),
    re_path('api/orders/createOrder', views.Order.as_view(), name='CreateOrder'),
    re_path('api/cars/allcars', views.CarsView.as_view(), name='cars'),
    re_path('api/cars/carbrands', views.CarBrandsView.as_view(), name='carbrands')
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
