"""
URL configuration for UI app.
"""

from django.urls import path

from . import views

app_name = 'ui'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('workflows/', views.workflows, name='workflows'),
    path('work-items/', views.work_items, name='work_items'),
    path('scheduling/', views.scheduling, name='scheduling'),
    path('profile/', views.profile, name='profile'),
    path('settings/', views.settings, name='settings'),
    path('search/', views.search, name='search'),
]
