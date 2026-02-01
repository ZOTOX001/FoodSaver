from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('directory/', views.ngo_directory, name='ngo_directory'),
    path('profile/<int:user_id>/', views.profile_view, name='profile_view'),
    path('connected-ngos/', views.connected_ngos, name='connected_ngos'),
]
