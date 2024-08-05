from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('advertisement/<int:pk>/', views.advertisement_detail, name='advertisement_detail'),
    path('advertisement/new/', views.create_advertisement, name='create_advertisement'),
    path('advertisement/<int:pk>/create_response/', views.create_response, name='create_response'),
    path('user/dashboard/', views.user_dashboard, name='user_dashboard'),
    path('delete_response/<int:pk>/', views.delete_response, name='delete_response'),
    path('accept_response/<int:pk>/', views.accept_response, name='accept_response'),
]
