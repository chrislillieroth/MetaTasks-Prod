"""
Tenancy helpers for multi-tenant operations.
"""


from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from apps.organizations.models import Organization

User = get_user_model()


def filter_by_organization(
    queryset: QuerySet,
    organization: Organization | None,
    org_field: str = "organization",
) -> QuerySet:
    """
    Filter a queryset by organization.

    Args:
        queryset: QuerySet to filter
        organization: Organization to filter by (None returns empty queryset)
        org_field: Name of the organization foreign key field

    Returns:
        Filtered QuerySet
    """
    if organization is None:
        return queryset.none()

    filter_kwargs = {org_field: organization}
    return queryset.filter(**filter_kwargs)


def ensure_organization_access(
    user: User,
    organization: Organization,
) -> bool:
    """
    Check if a user has access to an organization.

    Args:
        user: User to check
        organization: Organization to check access to

    Returns:
        True if user has access, False otherwise
    """
    if not user.is_authenticated:
        return False

    return organization.memberships.filter(
        user=user,
        is_active=True,
    ).exists()
