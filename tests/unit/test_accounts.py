"""
Tests for accounts models.
"""

import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
class TestUserModel:
    """Tests for the custom User model."""

    def test_create_user(self):
        """Test creating a basic user."""
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
        )
        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.check_password("testpass123")
        assert user.created_at is not None
        assert user.updated_at is not None

    def test_create_superuser(self):
        """Test creating a superuser."""
        user = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="adminpass123",
        )
        assert user.is_superuser
        assert user.is_staff

    def test_user_str(self):
        """Test user string representation."""
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
        )
        assert str(user) == "test@example.com"

    def test_email_unique(self):
        """Test that email must be unique."""
        User.objects.create_user(
            username="user1",
            email="test@example.com",
            password="pass123",
        )
        with pytest.raises(Exception):  # Will raise IntegrityError
            User.objects.create_user(
                username="user2",
                email="test@example.com",
                password="pass123",
            )
