"""
URL Configuration for MetaTasks project.
"""

from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    # Authentication
    path("accounts/login/", auth_views.LoginView.as_view(template_name='ui/accounts/login.html'), name='login'),
    path("accounts/logout/", auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    # UI routes
    path("", include("apps.ui.urls")),
    # API routes will be added in Phase 9
]

# Custom error handlers
handler404 = 'apps.ui.views.custom_404'
handler500 = 'apps.ui.views.custom_500'
