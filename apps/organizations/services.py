"""
Organization services - business logic for organization management.
"""


from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils.text import slugify

from apps.organizations.models import Membership, Organization

User = get_user_model()


@transaction.atomic
def create_organization(
    *,
    name: str,
    slug: str | None = None,
    description: str = "",
    owner: User,
) -> Organization:
    """
    Create a new organization with the given user as owner.

    Args:
        name: Organization name
        slug: URL-friendly slug (auto-generated if not provided)
        description: Optional organization description
        owner: User who will be the owner of the organization

    Returns:
        Created Organization instance
    """
    if not slug:
        slug = slugify(name)

    # Ensure unique slug
    base_slug = slug
    counter = 1
    while Organization.objects.filter(slug=slug).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1

    organization = Organization.objects.create(
        name=name,
        slug=slug,
        description=description,
    )

    # Create owner membership
    Membership.objects.create(
        user=owner,
        organization=organization,
        role=Membership.Role.OWNER,
    )

    return organization


@transaction.atomic
def add_member(
    *,
    organization: Organization,
    user: User,
    role: str = Membership.Role.MEMBER,
) -> Membership:
    """
    Add a user to an organization with the specified role.

    Args:
        organization: Organization to add the user to
        user: User to add
        role: Role to assign (default: MEMBER)

    Returns:
        Created Membership instance

    Raises:
        ValueError: If membership already exists
    """
    if Membership.objects.filter(user=user, organization=organization).exists():
        raise ValueError(f"User {user.email} is already a member of {organization.name}")

    membership = Membership.objects.create(
        user=user,
        organization=organization,
        role=role,
    )

    return membership


def remove_member(*, organization: Organization, user: User) -> None:
    """
    Remove a user from an organization.

    Args:
        organization: Organization to remove the user from
        user: User to remove
    """
    Membership.objects.filter(user=user, organization=organization).delete()


def update_member_role(
    *,
    organization: Organization,
    user: User,
    role: str,
) -> Membership:
    """
    Update a user's role in an organization.

    Args:
        organization: Organization the user belongs to
        user: User whose role to update
        role: New role to assign

    Returns:
        Updated Membership instance

    Raises:
        Membership.DoesNotExist: If membership doesn't exist
    """
    membership = Membership.objects.get(user=user, organization=organization)
    membership.role = role
    membership.save(update_fields=["role", "updated_at"])
    return membership
