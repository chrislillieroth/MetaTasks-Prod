"""
Licensing service layer for MetaTasks.

This module provides business logic for license enforcement and usage tracking.
"""

from typing import Any

from django.db import transaction
from django.db.models import F

from apps.common.exceptions import FeatureNotAvailable, PlanLimitExceeded
from apps.licensing.models import Plan, Usage
from apps.organizations.models import Organization


@transaction.atomic
def create_plan(
    name: str,
    plan_type: str,
    max_users: int,
    max_workflows: int,
    max_work_items: int,
    max_storage_bytes: int,
    description: str = "",
    **features: Any,
) -> Plan:
    """
    Create a new subscription plan.

    Args:
        name: Plan name
        plan_type: Plan type (free, starter, professional, enterprise)
        max_users: Maximum number of users (0 = unlimited)
        max_workflows: Maximum number of workflows (0 = unlimited)
        max_work_items: Maximum number of work items (0 = unlimited)
        max_storage_bytes: Maximum storage in bytes (0 = unlimited)
        description: Plan description
        **features: Boolean feature flags (has_api_access, has_integrations, etc.)

    Returns:
        Created Plan instance
    """
    plan = Plan.objects.create(
        name=name,
        plan_type=plan_type,
        description=description,
        max_users=max_users,
        max_workflows=max_workflows,
        max_work_items=max_work_items,
        max_storage_bytes=max_storage_bytes,
        has_api_access=features.get("has_api_access", True),
        has_integrations=features.get("has_integrations", False),
        has_advanced_workflows=features.get("has_advanced_workflows", False),
        has_priority_support=features.get("has_priority_support", False),
    )
    return plan


@transaction.atomic
def assign_plan(organization: Organization, plan: Plan) -> Usage:
    """
    Assign a plan to an organization.

    Creates or updates the Usage record for the organization.

    Args:
        organization: Organization to assign plan to
        plan: Plan to assign

    Returns:
        Usage instance
    """
    usage, created = Usage.objects.update_or_create(
        organization=organization,
        defaults={"plan": plan},
    )
    return usage


@transaction.atomic
def increment_usage(organization: Organization, metric: str, amount: int = 1) -> Usage:
    """
    Increment a usage metric for an organization.

    Args:
        organization: Organization to update usage for
        metric: Metric name (users_count, workflows_count, etc.)
        amount: Amount to increment by (default: 1)

    Returns:
        Updated Usage instance

    Raises:
        ValueError: If metric is invalid
    """
    valid_metrics = ["users_count", "workflows_count", "work_items_count", "storage_bytes"]
    if metric not in valid_metrics:
        raise ValueError(f"Invalid metric: {metric}. Must be one of {valid_metrics}")

    usage = Usage.objects.select_for_update().get(organization=organization)

    # Update the metric
    setattr(usage, metric, F(metric) + amount)
    usage.save(update_fields=[metric])

    # Refresh to get the actual value
    usage.refresh_from_db()

    return usage


@transaction.atomic
def decrement_usage(organization: Organization, metric: str, amount: int = 1) -> Usage:
    """
    Decrement a usage metric for an organization.

    Args:
        organization: Organization to update usage for
        metric: Metric name (users_count, workflows_count, etc.)
        amount: Amount to decrement by (default: 1)

    Returns:
        Updated Usage instance

    Raises:
        ValueError: If metric is invalid
    """
    valid_metrics = ["users_count", "workflows_count", "work_items_count", "storage_bytes"]
    if metric not in valid_metrics:
        raise ValueError(f"Invalid metric: {metric}. Must be one of {valid_metrics}")

    usage = Usage.objects.select_for_update().get(organization=organization)

    # Update the metric, ensuring it doesn't go below 0
    current = getattr(usage, metric)
    new_value = max(0, current - amount)
    setattr(usage, metric, new_value)
    usage.save(update_fields=[metric])

    return usage


def check_limit(organization: Organization, metric: str) -> bool:
    """
    Check if an organization is at or over a limit.

    Args:
        organization: Organization to check
        metric: Metric name (users_count, workflows_count, etc.)

    Returns:
        True if over limit, False otherwise
    """
    try:
        usage = Usage.objects.get(organization=organization)
        return usage.is_over_limit(metric)
    except Usage.DoesNotExist:
        # If no usage record exists, assume not over limit
        return False


def enforce_limit(organization: Organization, metric: str) -> None:
    """
    Enforce a limit for an organization.

    Args:
        organization: Organization to check
        metric: Metric name (users_count, workflows_count, etc.)

    Raises:
        PlanLimitExceeded: If the organization is at or over the limit
    """
    try:
        usage = Usage.objects.select_related("plan").get(organization=organization)
    except Usage.DoesNotExist:
        # If no usage record exists, allow the action
        return

    if usage.is_over_limit(metric):
        # Convert metric name to limit field name for error message
        if metric.endswith("_count"):
            limit_field = f"max_{metric[:-6]}"
        else:
            limit_field = f"max_{metric}"
        limit = getattr(usage.plan, limit_field)
        current = getattr(usage, metric)
        raise PlanLimitExceeded(metric, limit, current)


def check_feature(organization: Organization, feature: str) -> bool:
    """
    Check if a feature is available for an organization.

    Args:
        organization: Organization to check
        feature: Feature name (has_api_access, has_integrations, etc.)

    Returns:
        True if feature is available, False otherwise
    """
    try:
        usage = Usage.objects.select_related("plan").get(organization=organization)
        return getattr(usage.plan, feature, False)
    except Usage.DoesNotExist:
        # If no usage record exists, deny feature access
        return False


def enforce_feature(organization: Organization, feature: str) -> None:
    """
    Enforce feature availability for an organization.

    Args:
        organization: Organization to check
        feature: Feature name (has_api_access, has_integrations, etc.)

    Raises:
        FeatureNotAvailable: If the feature is not available in the plan
    """
    try:
        usage = Usage.objects.select_related("plan").get(organization=organization)
    except Usage.DoesNotExist:
        # If no usage record exists, deny feature access
        raise FeatureNotAvailable(feature, "No plan assigned")

    if not getattr(usage.plan, feature, False):
        raise FeatureNotAvailable(feature, usage.plan.name)
