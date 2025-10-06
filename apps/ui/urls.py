from django.urls import path
from . import views

app_name = 'ui'

urlpatterns = [
    # Main dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Search
    path('search/', views.search, name='search'),
    
    # User profile and settings
    path('profile/', views.profile, name='profile'),
    path('settings/', views.settings, name='settings'),
    
    # API endpoints
    path('api/notifications/', views.notifications_api, name='notifications_api'),
    
    # Health check
    path('health/', views.health_check, name='health_check'),
]