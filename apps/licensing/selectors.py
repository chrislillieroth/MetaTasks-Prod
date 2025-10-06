"""
Licensing selectors for MetaTasks.

This module provides query patterns for licensing data retrieval.
"""

from django.db.models import QuerySet

from apps.licensing.models import Plan, Usage
from apps.organizations.models import Organization


def get_organization_usage(organization: Organization) -> Usage | None:
    """
    Get usage information for an organization.

    Args:
        organization: Organization to get usage for

    Returns:
        Usage instance or None if not found
    """
    try:
        return Usage.objects.select_related("plan").get(organization=organization)
    except Usage.DoesNotExist:
        return None


def get_organization_plan(organization: Organization) -> Plan | None:
    """
    Get the plan for an organization.

    Args:
        organization: Organization to get plan for

    Returns:
        Plan instance or None if not found
    """
    usage = get_organization_usage(organization)
    return usage.plan if usage else None


def get_active_plans() -> QuerySet[Plan]:
    """
    Get all active plans.

    Returns:
        QuerySet of active Plan instances
    """
    return Plan.objects.filter(is_active=True)


def get_plan_by_type(plan_type: str) -> Plan | None:
    """
    Get a plan by its type.

    Args:
        plan_type: Plan type (free, starter, professional, enterprise)

    Returns:
        Plan instance or None if not found
    """
    try:
        return Plan.objects.get(plan_type=plan_type, is_active=True)
    except Plan.DoesNotExist:
        return None


def get_usage_stats(organization: Organization) -> dict[str, int | None]:
    """
    Get usage statistics for an organization.

    Args:
        organization: Organization to get stats for

    Returns:
        Dictionary with usage stats and remaining capacity
    """
    usage = get_organization_usage(organization)

    if not usage:
        return {
            "users_count": 0,
            "workflows_count": 0,
            "work_items_count": 0,
            "storage_bytes": 0,
            "users_remaining": None,
            "workflows_remaining": None,
            "work_items_remaining": None,
            "storage_remaining": None,
        }

    return {
        "users_count": usage.users_count,
        "workflows_count": usage.workflows_count,
        "work_items_count": usage.work_items_count,
        "storage_bytes": usage.storage_bytes,
        "users_remaining": usage.get_remaining("users_count"),
        "workflows_remaining": usage.get_remaining("workflows_count"),
        "work_items_remaining": usage.get_remaining("work_items_count"),
        "storage_remaining": usage.get_remaining("storage_bytes"),
    }
