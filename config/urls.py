"""
URL Configuration for MetaTasks project.
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.ui.urls")),
    # API routes will be added in Phase 9
]
