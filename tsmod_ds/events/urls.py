from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('win/', views.win),
    path('stat/', views.stat),
    path('registration/', views.register_new),
    path('last/', views.new_events_for_bot),
]
