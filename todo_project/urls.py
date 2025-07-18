"""
URL configuration for todo_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import include, path
from django.contrib.auth import views as auth_views
from todo_app import views as todo_app
from todo_app import views
from accounts import views
from images import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('accounts/', include('accounts.urls')), # accountsアプリのカスタムURL（signupなど）を読み込む
    path('accounts/', include('django.contrib.auth.urls')), # Djangoのlogin, logoutなどを読み込む
    path('login/', auth_views.LoginView.as_view(), name='registration/login'), # name='login' はNoReverseMatchを解決するのに重要
    path('todo/', include('todo_app.urls')),  # todo_app の URL 設定を include
    path('images/', include('images.urls')),  # images の URL 設定を include
    path('menu/', todo_app.menu, name='menu'),  # /todo/menu/

]
