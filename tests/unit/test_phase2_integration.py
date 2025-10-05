"""
Integration test for Phase 2: Accounts & Organizations.
Demonstrates the complete flow from user creation to organization management.
"""

import pytest
from django.contrib.auth import get_user_model

from apps.organizations import selectors, services
from apps.organizations.models import Membership

User = get_user_model()


@pytest.mark.django_db
class TestPhase2Integration:
    """Integration tests demonstrating Phase 2 functionality."""

    def test_complete_user_and_organization_workflow(self):
        """Test the complete workflow from user creation to organization management."""
        # Step 1: Create a business user
        owner = User.objects.create_user(
            username="business_owner",
            email="owner@business.com",
            password="securepass123",
        )
        assert owner.email == "owner@business.com"
        assert owner.is_active

        # Step 2: Create an organization with the user as owner
        org = services.create_organization(
            name="Acme Corporation",
            description="A test business organization",
            owner=owner,
        )
        assert org.name == "Acme Corporation"
        assert org.slug == "acme-corporation"
        assert org.is_active

        # Step 3: Verify owner membership was created
        owner_membership = selectors.get_user_membership(owner, org)
        assert owner_membership is not None
        assert owner_membership.role == Membership.Role.OWNER
        assert selectors.is_organization_owner(owner, org)
        assert selectors.is_organization_admin(owner, org)

        # Step 4: Create additional team members
        admin = User.objects.create_user(
            username="team_admin",
            email="admin@business.com",
            password="securepass123",
        )
        member = User.objects.create_user(
            username="team_member",
            email="member@business.com",
            password="securepass123",
        )
        viewer = User.objects.create_user(
            username="team_viewer",
            email="viewer@business.com",
            password="securepass123",
        )

        # Step 5: Add members with different roles
        services.add_member(
            organization=org,
            user=admin,
            role=Membership.Role.ADMIN,
        )
        services.add_member(
            organization=org,
            user=member,
            role=Membership.Role.MEMBER,
        )
        services.add_member(
            organization=org,
            user=viewer,
            role=Membership.Role.VIEWER,
        )

        # Step 6: Verify all members are in the organization
        members = list(selectors.get_organization_members(org))
        assert len(members) == 4
        assert owner in members
        assert admin in members
        assert member in members
        assert viewer in members

        # Step 7: Verify role-based permissions
        assert selectors.is_organization_admin(admin, org)
        assert not selectors.is_organization_admin(member, org)
        assert not selectors.is_organization_admin(viewer, org)

        # Step 8: Test role updates
        updated_membership = services.update_member_role(
            organization=org,
            user=member,
            role=Membership.Role.ADMIN,
        )
        assert updated_membership.role == Membership.Role.ADMIN
        assert selectors.is_organization_admin(member, org)

        # Step 9: Test member removal
        services.remove_member(organization=org, user=viewer)
        remaining_members = list(selectors.get_organization_members(org))
        assert len(remaining_members) == 3
        assert viewer not in remaining_members

        # Step 10: Verify user can see their organizations
        owner_orgs = list(selectors.get_user_organizations(owner))
        assert len(owner_orgs) == 1
        assert org in owner_orgs

        # Step 11: Create a second organization for the same user
        second_org = services.create_organization(
            name="Second Business",
            owner=owner,
        )
        owner_orgs = list(selectors.get_user_organizations(owner))
        assert len(owner_orgs) == 2
        assert org in owner_orgs
        assert second_org in owner_orgs

        # Step 12: Verify default organization (first one created)
        default_org = selectors.get_user_default_organization(owner)
        assert default_org == org

    def test_multi_tenant_scenario(self):
        """Test multi-tenant scenario with separate organizations."""
        # Create two separate organizations
        user1 = User.objects.create_user(
            username="user1", email="user1@test.com", password="pass"
        )
        user2 = User.objects.create_user(
            username="user2", email="user2@test.com", password="pass"
        )

        org1 = services.create_organization(name="Organization 1", owner=user1)
        org2 = services.create_organization(name="Organization 2", owner=user2)

        # Verify isolation: user1 cannot access org2 and vice versa
        assert selectors.get_user_membership(user1, org2) is None
        assert selectors.get_user_membership(user2, org1) is None

        # Verify each user only sees their own organization
        user1_orgs = list(selectors.get_user_organizations(user1))
        user2_orgs = list(selectors.get_user_organizations(user2))

        assert len(user1_orgs) == 1
        assert org1 in user1_orgs
        assert org2 not in user1_orgs

        assert len(user2_orgs) == 1
        assert org2 in user2_orgs
        assert org1 not in user2_orgs

        # Cross-organization membership
        services.add_member(organization=org1, user=user2, role=Membership.Role.MEMBER)

        # Now user2 should see both organizations
        user2_orgs = list(selectors.get_user_organizations(user2))
        assert len(user2_orgs) == 2
        assert org1 in user2_orgs
        assert org2 in user2_orgs

        # But user2 is only owner of org2
        assert selectors.is_organization_owner(user2, org2)
        assert not selectors.is_organization_owner(user2, org1)
