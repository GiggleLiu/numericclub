from django.urls import path
from . import views

urlpatterns = [
    # Examples:
    path(r'logout/', views.logout, name='logout'),
    path(r'login/', views.login, name='login'),
    path(r'user_detail/<int:user_id>/', views.user_detail, name='user_detail'),
    path(r'user_update/', views.user_update, name='user_update'),
    path(r'being_update/', views.being_update, name='being_update'),
    path(r'register_step1/', views.register_step1, name='register_step1'),
    path(r'register_step2/', views.register_step2, name='register_step2'),
    path(r'register_success/', views.register_success, name='register_success'),
    path(r'register_step2/<int:user_id>/', views.register_step2,
         name='redirectto_register_step2'),
    path(r'update_password/', views.update_password, name='update_password'),
]
