from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('advertisement/<int:pk>/', views.advertisement_detail, name='advertisement_detail'),
    path('advertisement/new/', views.create_advertisement, name='create_advertisement'),
    path('advertisement/<int:pk>/respond/', views.create_response, name='create_response'),
]
