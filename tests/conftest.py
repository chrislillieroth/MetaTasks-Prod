"""
Pytest configuration and fixtures for MetaTasks tests.
"""

import pytest


@pytest.fixture
def sample_user(db):
    """Create a sample user for testing."""
    from apps.accounts.models import User

    return User.objects.create_user(
        username="testuser", email="test@example.com", password="testpass123"
    )
