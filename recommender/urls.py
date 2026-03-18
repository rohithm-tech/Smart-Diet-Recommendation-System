from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile_setup/', views.profile_setup, name='profile_setup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('log_food/', views.log_food, name='log_food'),
    path('export_pdf/', views.export_plan_pdf, name='export_plan_pdf'),
]
