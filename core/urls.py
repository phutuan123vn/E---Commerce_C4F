"""
URL configuration for core project.

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
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls

from core import settings
from core import views


urlpatterns = [
    path("", include(([
                path("login/", views.LoginView.as_view(), name="login"),
                path("register/", views.CreateUsersView.as_view(), name="register"),
                path("test/", views.testAPI, name="test"),
            ], "core"), namespace="core")
        ),
    path("admin/", admin.site.urls),
    path("api/", include(("shop.urls", "shop"), namespace="shop")),
    path("api/", include(("inventory.urls", "inventory"), namespace="inventory")),
]

if settings.DEBUG:
    urlpatterns += debug_toolbar_urls()
