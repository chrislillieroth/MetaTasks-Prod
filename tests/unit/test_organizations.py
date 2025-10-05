"""
Tests for organization models, services, and selectors.
"""

import pytest
from django.contrib.auth import get_user_model

from apps.organizations.models import Membership, Organization
from apps.organizations import services, selectors

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
        description="A test organization",
        owner=user,
    )


@pytest.mark.django_db
class TestOrganizationModel:
    """Tests for the Organization model."""

    def test_create_organization_directly(self):
        """Test creating an organization directly."""
        org = Organization.objects.create(
            name="Test Org",
            slug="test-org",
            description="A test organization",
        )
        assert org.name == "Test Org"
        assert org.slug == "test-org"
        assert org.is_active is True
        assert org.created_at is not None
        assert org.updated_at is not None

    def test_organization_str(self):
        """Test organization string representation."""
        org = Organization.objects.create(name="Test Org", slug="test-org")
        assert str(org) == "Test Org"


@pytest.mark.django_db
class TestMembershipModel:
    """Tests for the Membership model."""

    def test_create_membership(self, another_user):
        """Test creating a membership."""
        # Create organization without using the service (to avoid creating a membership)
        organization = Organization.objects.create(
            name="Test Org",
            slug="test-org",
        )
        
        membership = Membership.objects.create(
            user=another_user,
            organization=organization,
            role=Membership.Role.MEMBER,
        )
        assert membership.user == another_user
        assert membership.organization == organization
        assert membership.role == Membership.Role.MEMBER
        assert membership.is_active is True

    def test_membership_str(self, another_user):
        """Test membership string representation."""
        # Create organization without using the service
        organization = Organization.objects.create(
            name="Test Org",
            slug="test-org",
        )
        
        membership = Membership.objects.create(
            user=another_user,
            organization=organization,
            role=Membership.Role.OWNER,
        )
        assert str(membership) == f"{another_user.email} - {organization.name} (owner)"

    def test_membership_unique_together(self, another_user):
        """Test that user-organization combination must be unique."""
        # Create organization without using the service
        organization = Organization.objects.create(
            name="Test Org",
            slug="test-org",
        )
        
        Membership.objects.create(
            user=another_user,
            organization=organization,
            role=Membership.Role.MEMBER,
        )
        with pytest.raises(Exception):  # Will raise IntegrityError
            Membership.objects.create(
                user=another_user,
                organization=organization,
                role=Membership.Role.ADMIN,
            )


@pytest.mark.django_db
class TestOrganizationServices:
    """Tests for organization services."""

    def test_create_organization(self, user):
        """Test creating an organization with owner."""
        org = services.create_organization(
            name="New Organization",
            description="A new organization",
            owner=user,
        )
        assert org.name == "New Organization"
        assert org.slug == "new-organization"
        assert org.description == "A new organization"
        assert org.is_active is True

        # Check owner membership was created
        membership = Membership.objects.get(user=user, organization=org)
        assert membership.role == Membership.Role.OWNER
        assert membership.is_active is True

    def test_create_organization_with_custom_slug(self, user):
        """Test creating an organization with a custom slug."""
        org = services.create_organization(
            name="My Organization",
            slug="custom-slug",
            owner=user,
        )
        assert org.slug == "custom-slug"

    def test_create_organization_slug_auto_increment(self, user):
        """Test that duplicate slugs are auto-incremented."""
        org1 = services.create_organization(
            name="Test Org",
            owner=user,
        )
        assert org1.slug == "test-org"

        org2 = services.create_organization(
            name="Test Org",
            owner=user,
        )
        assert org2.slug == "test-org-1"

        org3 = services.create_organization(
            name="Test Org",
            owner=user,
        )
        assert org3.slug == "test-org-2"

    def test_add_member(self, organization, another_user):
        """Test adding a member to an organization."""
        membership = services.add_member(
            organization=organization,
            user=another_user,
            role=Membership.Role.MEMBER,
        )
        assert membership.user == another_user
        assert membership.organization == organization
        assert membership.role == Membership.Role.MEMBER

    def test_add_member_with_admin_role(self, organization, another_user):
        """Test adding a member with admin role."""
        membership = services.add_member(
            organization=organization,
            user=another_user,
            role=Membership.Role.ADMIN,
        )
        assert membership.role == Membership.Role.ADMIN

    def test_add_member_duplicate_raises_error(self, organization, user):
        """Test that adding an existing member raises an error."""
        # user is already owner from the organization fixture
        with pytest.raises(ValueError, match="already a member"):
            services.add_member(
                organization=organization,
                user=user,
                role=Membership.Role.MEMBER,
            )

    def test_remove_member(self, organization, another_user):
        """Test removing a member from an organization."""
        services.add_member(
            organization=organization,
            user=another_user,
        )
        assert Membership.objects.filter(
            user=another_user, organization=organization
        ).exists()

        services.remove_member(
            organization=organization,
            user=another_user,
        )
        assert not Membership.objects.filter(
            user=another_user, organization=organization
        ).exists()

    def test_update_member_role(self, organization, another_user):
        """Test updating a member's role."""
        services.add_member(
            organization=organization,
            user=another_user,
            role=Membership.Role.MEMBER,
        )

        membership = services.update_member_role(
            organization=organization,
            user=another_user,
            role=Membership.Role.ADMIN,
        )
        assert membership.role == Membership.Role.ADMIN

    def test_update_member_role_not_found(self, organization, another_user):
        """Test updating role for non-existent membership raises error."""
        with pytest.raises(Membership.DoesNotExist):
            services.update_member_role(
                organization=organization,
                user=another_user,
                role=Membership.Role.ADMIN,
            )


@pytest.mark.django_db
class TestOrganizationSelectors:
    """Tests for organization selectors."""

    def test_get_user_organizations(self, user, organization):
        """Test getting organizations for a user."""
        orgs = selectors.get_user_organizations(user)
        assert organization in orgs
        assert len(orgs) == 1

    def test_get_user_organizations_multiple(self, user):
        """Test getting multiple organizations for a user."""
        org1 = services.create_organization(name="Org 1", owner=user)
        org2 = services.create_organization(name="Org 2", owner=user)

        orgs = list(selectors.get_user_organizations(user))
        assert len(orgs) == 2
        assert org1 in orgs
        assert org2 in orgs

    def test_get_user_organizations_excludes_inactive(self, user, organization):
        """Test that inactive organizations are excluded."""
        organization.is_active = False
        organization.save()

        orgs = selectors.get_user_organizations(user)
        assert organization not in orgs

    def test_get_organization_members(self, organization, user, another_user):
        """Test getting members of an organization."""
        services.add_member(organization=organization, user=another_user)

        members = list(selectors.get_organization_members(organization))
        assert len(members) == 2
        assert user in members
        assert another_user in members

    def test_get_user_membership(self, user, organization):
        """Test getting a user's membership."""
        membership = selectors.get_user_membership(user, organization)
        assert membership is not None
        assert membership.user == user
        assert membership.organization == organization
        assert membership.role == Membership.Role.OWNER

    def test_get_user_membership_not_found(self, another_user, organization):
        """Test getting membership for non-member returns None."""
        membership = selectors.get_user_membership(another_user, organization)
        assert membership is None

    def test_get_user_default_organization(self, user, organization):
        """Test getting a user's default organization."""
        default_org = selectors.get_user_default_organization(user)
        assert default_org == organization

    def test_get_user_default_organization_none(self, another_user):
        """Test getting default organization for user with no orgs."""
        default_org = selectors.get_user_default_organization(another_user)
        assert default_org is None

    def test_is_organization_owner(self, user, organization):
        """Test checking if user is organization owner."""
        assert selectors.is_organization_owner(user, organization) is True

    def test_is_organization_owner_false(self, another_user, organization):
        """Test checking if non-owner is owner."""
        assert selectors.is_organization_owner(another_user, organization) is False

    def test_is_organization_admin_owner(self, user, organization):
        """Test that owner is considered admin."""
        assert selectors.is_organization_admin(user, organization) is True

    def test_is_organization_admin_admin_role(self, organization, another_user):
        """Test that admin role is considered admin."""
        services.add_member(
            organization=organization,
            user=another_user,
            role=Membership.Role.ADMIN,
        )
        assert selectors.is_organization_admin(another_user, organization) is True

    def test_is_organization_admin_member_false(self, organization, another_user):
        """Test that regular member is not admin."""
        services.add_member(
            organization=organization,
            user=another_user,
            role=Membership.Role.MEMBER,
        )
        assert selectors.is_organization_admin(another_user, organization) is False
