"""
Tests for common middleware and tenancy helpers.
"""

import pytest
from django.contrib.auth import get_user_model
from django.http import HttpRequest
from django.test import RequestFactory

from apps.common.middleware import ActiveOrganizationMiddleware
from apps.common.tenancy import ensure_organization_access, filter_by_organization
from apps.organizations.models import Organization
from apps.organizations import services

User = get_user_model()


@pytest.fixture
def user():
    """Create a test user."""
    return User.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="testpass123",
    )


@pytest.fixture
def another_user():
    """Create another test user."""
    return User.objects.create_user(
        username="anotheruser",
        email="another@example.com",
        password="testpass123",
    )


@pytest.fixture
def organization(user):
    """Create a test organization."""
    return services.create_organization(
        name="Test Organization",
        owner=user,
    )


@pytest.fixture
def request_factory():
    """Create a request factory."""
    return RequestFactory()


@pytest.mark.django_db
class TestActiveOrganizationMiddleware:
    """Tests for the ActiveOrganizationMiddleware."""

    def test_middleware_with_unauthenticated_user(self, request_factory):
        """Test middleware with unauthenticated user."""
        request = request_factory.get("/")
        request.user = None
        request.session = {}

        def get_response(req):
            return req

        middleware = ActiveOrganizationMiddleware(get_response)
        middleware(request)

        assert request.active_org is None

    def test_middleware_with_authenticated_user_no_orgs(
        self, request_factory, another_user
    ):
        """Test middleware with authenticated user who has no organizations."""
        request = request_factory.get("/")
        request.user = another_user
        request.session = {}

        def get_response(req):
            return req

        middleware = ActiveOrganizationMiddleware(get_response)
        middleware(request)

        assert request.active_org is None

    def test_middleware_with_default_organization(
        self, request_factory, user, organization
    ):
        """Test middleware falls back to user's default organization."""
        request = request_factory.get("/")
        request.user = user
        request.session = {}

        def get_response(req):
            return req

        middleware = ActiveOrganizationMiddleware(get_response)
        middleware(request)

        assert request.active_org == organization

    def test_middleware_with_session_organization(
        self, request_factory, user, organization
    ):
        """Test middleware uses organization from session."""
        request = request_factory.get("/")
        request.user = user
        request.session = {"active_organization_id": organization.id}

        def get_response(req):
            return req

        middleware = ActiveOrganizationMiddleware(get_response)
        middleware(request)

        assert request.active_org == organization

    def test_middleware_with_header_organization(
        self, request_factory, user, organization
    ):
        """Test middleware uses organization from header."""
        request = request_factory.get(
            "/", HTTP_X_ORGANIZATION_ID=str(organization.id)
        )
        request.user = user
        request.session = {}

        def get_response(req):
            return req

        middleware = ActiveOrganizationMiddleware(get_response)
        middleware(request)

        assert request.active_org == organization

    def test_middleware_ignores_invalid_session_org(
        self, request_factory, user, organization
    ):
        """Test middleware ignores invalid organization ID in session."""
        request = request_factory.get("/")
        request.user = user
        request.session = {"active_organization_id": 99999}  # Non-existent ID

        def get_response(req):
            return req

        middleware = ActiveOrganizationMiddleware(get_response)
        middleware(request)

        # Should fall back to default organization
        assert request.active_org == organization
        # Session should be cleaned up
        assert "active_organization_id" not in request.session

    def test_middleware_verifies_user_access(
        self, request_factory, user, another_user, organization
    ):
        """Test middleware verifies user has access to the organization."""
        # Create another organization
        other_org = services.create_organization(
            name="Other Organization",
            owner=another_user,
        )

        # Try to use other_org with user (who doesn't have access)
        request = request_factory.get("/")
        request.user = user
        request.session = {"active_organization_id": other_org.id}

        def get_response(req):
            return req

        middleware = ActiveOrganizationMiddleware(get_response)
        middleware(request)

        # Should fall back to user's own organization
        assert request.active_org == organization


@pytest.mark.django_db
class TestTenancyHelpers:
    """Tests for tenancy helper functions."""

    def test_filter_by_organization(self, organization):
        """Test filtering queryset by organization."""
        # Create test data with organization foreign keys
        # For this test, we'll use the Membership model which has organization FK
        from apps.organizations.models import Membership
        from django.contrib.auth import get_user_model

        User = get_user_model()
        user1 = User.objects.create_user(username="user1", email="user1@test.com")
        user2 = User.objects.create_user(username="user2", email="user2@test.com")

        org1 = Organization.objects.create(name="Org 1", slug="org-1")
        org2 = Organization.objects.create(name="Org 2", slug="org-2")

        # Create memberships
        Membership.objects.create(user=user1, organization=org1)
        Membership.objects.create(user=user2, organization=org2)

        # Filter by org1
        queryset = Membership.objects.all()
        filtered = filter_by_organization(queryset, org1)

        assert filtered.count() == 1
        assert filtered.first().organization == org1

    def test_filter_by_organization_none_returns_empty(self):
        """Test that None organization returns empty queryset."""
        queryset = Organization.objects.all()
        filtered = filter_by_organization(queryset, None)
        assert filtered.count() == 0

    def test_ensure_organization_access_authenticated(self, user, organization):
        """Test ensuring user has access to organization."""
        assert ensure_organization_access(user, organization) is True

    def test_ensure_organization_access_no_access(self, another_user, organization):
        """Test user without access returns False."""
        assert ensure_organization_access(another_user, organization) is False

    def test_ensure_organization_access_unauthenticated(
        self, organization, request_factory
    ):
        """Test unauthenticated user returns False."""
        # Create an anonymous user
        from django.contrib.auth.models import AnonymousUser

        anon_user = AnonymousUser()
        assert ensure_organization_access(anon_user, organization) is False
