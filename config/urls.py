"""
URL Configuration for MetaTasks project.
"""

from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    # Authentication
    path("login/", auth_views.LoginView.as_view(template_name='ui/auth/login.html'), name='login'),
    path("logout/", auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    # UI routes
    path("", include("apps.ui.urls")),
    # API routes will be added in Phase 9
]
