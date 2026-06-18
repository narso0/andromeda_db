from django.urls import path
from core import views

urlpatterns = [
    path('', views.home, name='home'),
    path('samples/', views.sample_list, name='sample_list'),
    path('samples/add/', views.add_sample, name='add_sample'),
    path('users/', views.user_list, name='user_list'),
    path('users/add/', views.add_user, name='add_user'),
]