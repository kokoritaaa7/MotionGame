from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from . import views

urlpatterns = [
    path('', views.index, name=''),
    path('tour_sing/', views.tour_sing, name='sing'),
    path('landmark_data/', views.landmark_data, name='landmark'),
    path('ranking_board/', views.ranking_board, name='ranking'),
    path('sendScore', views.sendScore),
    path('us/', views.us),
    path('cart/', views.cart),
    path('checkout/', views.checkout),
    path('contact/', views.contact),
    path('error/', views.error),
    path('features/', views.features),
    path('login/', views.login),
    path('profile/', views.profile),
    path('registration/', views.registration),
    path('shopdetail/', views.shopdetail),
    path('shop/', views.shop),
    path('tourna/', views.tourna),
    path('tour/', views.tour),

]