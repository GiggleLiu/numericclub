from django.urls import path
from . import views

urlpatterns = [
    # Examples:
    path(r'logout/', views.logout, name='logout'),
    path(r'login/', views.login, name='login'),
    path(r'<int:pk>/', views.DetailView.as_view(), name='user_detail'),
    path(r'list/', views.ListView.as_view(), name='user_list'),
    path(r'user_update/', views.user_update, name='user_update'),
    path(r'register/', views.register, name='register'),
    path(r'delete/', views.user_delete, name='delete'),
    path(r'register_success/', views.register_success, name='register_success'),
    path(r'update_password/', views.update_password, name='update_password'),
]
