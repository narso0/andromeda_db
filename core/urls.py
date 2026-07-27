from django.urls import path
from core import views

urlpatterns = [
    path('', views.home, name='home'),
    path('samples/', views.sample_list, name='sample_list'),
    path('samples/add/', views.add_sample, name='add_sample'),
    path('users/', views.user_list, name='user_list'),
    path('users/add/', views.add_user, name='add_user'),
    path('samples/<int:pk>/', views.SampleDetailView.as_view(), name='sample_detail'),
    path('acquisitions/<str:pk>/', views.AcquisitionDetailView.as_view(), name='acquisition_detail'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user_detail'),
]