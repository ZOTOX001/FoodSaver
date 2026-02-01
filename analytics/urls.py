from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('leaderboard/', views.leaderboard_view, name='leaderboard'),
    path('predict/', views.predict_surplus, name='predict_surplus'),
]
