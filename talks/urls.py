"""numericclub URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path
from . import views

urlpatterns = [
    path('archive/', views.ListView.as_view(), name='archive'),
    path('user/<int:pk>/', views.archive_user, name='archive_user'),
    path('me/', views.archive_me, name='archive_me'),
    path('current/', views.current, name='current'),
    path('new/<int:topic_id>/', views.talk_new, name='new'),
    path('delete/<int:pk>/', views.talk_delete, name='delete'),
    path('publish/<int:pk>/', views.talk_publish, name='publish'),
    path('inform/<int:pk>/', views.talk_inform, name='inform'),
    path('unpublish/<int:pk>/', views.talk_unpublish, name='unpublish'),
    path('update/<int:pk>/', views.talk_update, name='update'),
    path('<int:pk>/', views.talk_detail, name='detail'),
]
