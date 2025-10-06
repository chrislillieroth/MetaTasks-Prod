"""
UI app views.
"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def dashboard(request):
    """
    Main dashboard view.
    """
    context = {
        "page_title": "Dashboard",
        "usage_current": 750,
        "usage_limit": 1000,
    }
    return render(request, "ui/pages/dashboard.html", context)


def index(request):
    """
    Landing/index page.
    """
    return render(request, "ui/pages/index.html")
