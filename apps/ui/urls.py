"""
URL configuration for UI app.
"""

from django.urls import path
from . import views

app_name = 'ui'

urlpatterns = [
    # Dashboard
    path('', views.DashboardView.as_view(), name='dashboard'),
    
    # Workflows
    path('workflows/', views.WorkflowListView.as_view(), name='workflows'),
    
    # Organizations
    path('organizations/', views.OrganizationListView.as_view(), name='organizations'),
    
    # Scheduling
    path('scheduling/', views.SchedulingView.as_view(), name='scheduling'),
    
    # Integrations
    path('integrations/', views.IntegrationsView.as_view(), name='integrations'),
    
    # Licensing
    path('licensing/', views.LicensingView.as_view(), name='licensing'),
    
    # Analytics
    path('analytics/', views.AnalyticsView.as_view(), name='analytics'),
    
    # Account
    path('account/', views.AccountView.as_view(), name='account'),
    path('settings/', views.SettingsView.as_view(), name='settings'),
]
