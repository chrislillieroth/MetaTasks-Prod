"""
URL Configuration for MetaTasks project.
"""

from django.contrib import admin
from django.urls import path

urlpatterns = [
    path("admin/", admin.site.urls),
    # API routes will be added in Phase 9
    # UI routes will be added in Phase 10
]
