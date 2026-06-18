from django.urls import path
from core import views

urlpatterns = [
    path('', views.sample_list, name='sample_list'),
    path('add/', views.add_sample, name='add_sample'),
]