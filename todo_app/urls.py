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
from . import views

app_name = 'todo_app'

urlpatterns = [
    path('todo_list', views.todo_list, name='todo_list'),  # /todo/
        
    #TodoCreate
    path('create/', views.Todo_Create, name='todo_create'),  # /todo/create/
    path('create/process/<uuid:pk>/', views.Todo_Create, name='todo_create_process'), # /todo/create/process/uuid/
    path('create/confirm/', views.Todo_Create_confirm, name='todo_create_confirm'), # /todo/create/confirm/
    path('create/execute/', views.Todo_Create_execute, name='todo_create_execute'), # /todo/create/execute/
    
    #TodoUpdate
    path('update/<uuid:pk>/', views.Todo_Update_view, name='todo_update'),  # /todo/update/uuid/
    path('update/confirm/display/<uuid:pk>/', views.Todo_Update_confirm, name='todo_update_confirm_display'),
    path('update/execute/<uuid:pk>/', views.Todo_Update_execute, name='todo_update_execute'), # /todo/update/execute/

    #Tododelete
    path('delete/<uuid:pk>/', views.Todo_delete_view, name='todo_delete'),  # /todo/delete/uuid/
]
