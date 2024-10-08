"""
URL configuration for publicidad project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.urls import include

from .views import LandingPage, Publicidad, CustomLoginView
from . import views
from django.contrib.auth import views as auth_views
from .views import heartbeat

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',LandingPage.as_view(),name='Landing_page'),
    path('publicidad',Publicidad.as_view(),name='publicidad'),
    path('publicidad/', include('publiApp.urls')),
    path('accounts/',include('django.contrib.auth.urls')),
    path('loginview/',CustomLoginView.as_view(),name='loginview'),
    path('api/heartbeat/', heartbeat, name='heartbeat'),
]

