"""
Basic smoke test to verify Django setup.
"""

import pytest
from django.conf import settings


def test_settings_configured():
    """Test that Django settings are properly configured."""
    assert settings.configured
    assert settings.SECRET_KEY is not None


@pytest.mark.django_db
def test_user_model_exists(sample_user):
    """Test that the User model can be created."""
    assert sample_user.email == "test@example.com"
    assert sample_user.username == "testuser"
