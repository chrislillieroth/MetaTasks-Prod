"""
URL Configuration for MetaTasks project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    
    # Main UI routes
    path("", include("apps.ui.urls")),
    
    # App-specific routes
    path("workflows/", include("apps.workflows.urls")),
    path("organizations/", include("apps.organizations.urls")),
    path("scheduling/", include("apps.scheduling.urls")),
    path("analytics/", include("apps.analytics.urls")),
    path("integrations/", include("apps.integrations.urls")),
    path("accounts/", include("apps.accounts.urls")),
    path("billing/", include("apps.billing.urls")),
    path("notifications/", include("apps.notifications.urls")),
    path("audit/", include("apps.audit.urls")),
    
    # API routes (for HTMX and AJAX)
    path("api/", include("apps.api.urls")),
]

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
