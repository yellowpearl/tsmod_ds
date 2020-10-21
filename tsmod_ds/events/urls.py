from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('win/', views.win),
    path('stat/', views.stat),
    path('registration/', views.register_new),
    path('last/', views.new_events_for_bot),
    path('wipe/', views.wipe_rating),
    path('leaderboard/', views.leaderboard),
]
