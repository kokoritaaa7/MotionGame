from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from . import views

urlpatterns = [
    path('us/', views.us),
    path('cart/', views.cart),
    path('check/', views.check),
    path('tact/', views.tact),
    path('error/', views.err),
    path('fea/', views.fea),
    path('ind/', views.ind),
    path('log/', views.log),
    path('pro/', views.pro),
    path('ragist/', views.ragist),
    path('shopdetail/', views.shopdetail),
    path('shop/', views.shop),
    path('tourna/', views.tourna),
    path('tour/', views.tour),
    path('tour_sing/', views.tour_sing),
    path('landmark_data/', views.landmark_data),
]