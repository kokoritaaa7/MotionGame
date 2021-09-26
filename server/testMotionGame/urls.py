from django.urls import path
from django.urls.conf import include
from . import views

urlpatterns = [
    path('', views.home),
    path('landmark_data/', views.landmark_data),
    path('ranking_board/', views.ranking_board),
]