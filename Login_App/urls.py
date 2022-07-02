from django.urls import path
from . import views

app_name = 'Login_App'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('profile/', views.user_profile, name='user_profile'),
    path('profile_update/', views.user_info_update, name='user_info_update'),
    path('password_change/', views.user_password_change, name='user_password_change'),
    path('[picture_add]/', views.add_profile_picture, name='picture_add'),
    path('picture_change/', views.change_picture, name='picture_change'),
    path('user_info/<str:user>', views.public_user_info, name='public_user_info'),
    path('check_password', views.password_check, name='password_check'),
    path('user-delete/<pk>/', views.UserDelete.as_view(), name='user_delete'),
]
