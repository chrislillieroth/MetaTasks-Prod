"""
Settings for generating migrations (uses SQLite).
"""

from .base import *  # noqa: F403, F401

# Use SQLite for migrations
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",  # noqa: F405
    }
}

# Secret key for migrations
SECRET_KEY = "migrations-secret-key-not-for-production"

# Debug mode
DEBUG = True

# Allowed hosts
ALLOWED_HOSTS = ["*"]
