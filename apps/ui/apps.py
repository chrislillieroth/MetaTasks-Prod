"""
UI app configuration.
"""

from django.apps import AppConfig


class UiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.ui"
    label = "ui"
