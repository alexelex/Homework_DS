"""shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from shop import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('database/product', views.product_info),
    path('database/product/delete', views.product_delete),
    path('database/product/edit', views.product_edit),
    path('database/product/create', views.product_create),
    path('database/products_list', views.products_list),
    # path('product/create/?', views.product_create, name='product_create'),
    # path('product/<slug:product>/__delete__/?', views.product_delete, name='product_delete'),
    # path('product/<slug:product>/__edit__/?', views.product_edit, name='product_edit'),
    # path('product/<slug:product>/__info__/?', views.product_info, name='product_info'),
    # path('product/list/?', views.products_list, name='products_list'),
]
