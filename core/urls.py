from django.urls import path
from core import views

urlpatterns = [
    path('', views.sample_list, name='sample_list'),
]