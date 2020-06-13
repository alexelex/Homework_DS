"""authorization URL Configuration

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
import os
import sys
from django.contrib import admin
from django.urls import path
from . import views
from . import grpc

urlpatterns = [
    path('admin/', admin.site.urls),
    path('registration', views.registration),
    path('activation', views.activation),
    path('authorization', views.authorization),
    path('update_token', views.update_token),
    path('validation', views.validation),
    path('promotion', views.promotion),
]

if os.environ.get("WITH_GRPC"):
    # https://stackoverflow.com/questions/31291608/effect-of-using-sys-path-insert0-path-and-sys-pathappend-when-loading-modul
    sys.path.insert(0, "..")
    def grpc_handlers(server):
        grpc.handlers(server)