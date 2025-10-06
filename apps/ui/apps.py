# MetaTasks UI App Configuration

from django.apps import AppConfig


class UiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.ui'
    verbose_name = 'User Interface'
    
    def ready(self):
        """Application ready setup."""
        # Import any signals or startup code here
        pass
