from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('room/<str:pk>/', views.room, name='room'),
    path('create-room/', views.create_room, name='create-room'),
    # path('room/<str:pk>/', views.room, name='room'),
    # path('room/<str:pk>/', views.room, name='room'),
    # path('room/<str:pk>/', views.room, name='room'),
    # path('room/<str:pk>/', views.room, name='room'),
]
