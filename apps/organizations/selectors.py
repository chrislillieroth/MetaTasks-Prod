"""
Organization selectors - query patterns for organization data.
"""


from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from apps.organizations.models import Membership, Organization

User = get_user_model()


def get_user_organizations(user: User) -> QuerySet[Organization]:
    """
    Get all organizations a user belongs to.

    Args:
        user: User to get organizations for

    Returns:
        QuerySet of Organizations
    """
    return Organization.objects.filter(
        memberships__user=user,
        memberships__is_active=True,
        is_active=True,
    ).distinct()


def get_organization_members(organization: Organization) -> QuerySet[User]:
    """
    Get all active members of an organization.

    Args:
        organization: Organization to get members for

    Returns:
        QuerySet of Users
    """
    return User.objects.filter(
        memberships__organization=organization,
        memberships__is_active=True,
    ).distinct()


def get_user_membership(
    user: User,
    organization: Organization,
) -> Membership | None:
    """
    Get a user's membership in an organization.

    Args:
        user: User to get membership for
        organization: Organization to check membership in

    Returns:
        Membership instance or None if not found
    """
    try:
        return Membership.objects.get(
            user=user,
            organization=organization,
            is_active=True,
        )
    except Membership.DoesNotExist:
        return None


def get_user_default_organization(user: User) -> Organization | None:
    """
    Get a user's default organization (first active membership).

    Args:
        user: User to get default organization for

    Returns:
        Organization instance or None if user has no organizations
    """
    organizations = get_user_organizations(user)
    return organizations.first()


def is_organization_owner(user: User, organization: Organization) -> bool:
    """
    Check if a user is an owner of an organization.

    Args:
        user: User to check
        organization: Organization to check ownership of

    Returns:
        True if user is owner, False otherwise
    """
    return Membership.objects.filter(
        user=user,
        organization=organization,
        role=Membership.Role.OWNER,
        is_active=True,
    ).exists()


def is_organization_admin(user: User, organization: Organization) -> bool:
    """
    Check if a user is an admin (owner or admin role) of an organization.

    Args:
        user: User to check
        organization: Organization to check admin status of

    Returns:
        True if user is owner or admin, False otherwise
    """
    return Membership.objects.filter(
        user=user,
        organization=organization,
        role__in=[Membership.Role.OWNER, Membership.Role.ADMIN],
        is_active=True,
    ).exists()
