"""
Licensing decorators for MetaTasks.

This module provides decorators for enforcing plan limits and feature availability.
"""

from collections.abc import Callable
from functools import wraps
from typing import Any

from apps.licensing import services
from apps.organizations.models import Organization


def require_feature(feature: str) -> Callable:
    """
    Decorator to enforce feature availability.

    Usage:
        @require_feature('has_api_access')
        def my_api_view(request, organization):
            ...

    Args:
        feature: Feature name to check (e.g., 'has_api_access')

    Raises:
        FeatureNotAvailable: If the feature is not available
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Try to find organization in args or kwargs
            organization = None

            # Check kwargs first
            if "organization" in kwargs:
                organization = kwargs["organization"]
            elif "org" in kwargs:
                organization = kwargs["org"]

            # Check args (look for Organization instances)
            if not organization:
                for arg in args:
                    if isinstance(arg, Organization):
                        organization = arg
                        break

            # Check if request object has active_org (from middleware)
            if not organization:
                for arg in args:
                    if hasattr(arg, "active_org"):
                        organization = arg.active_org
                        break

            if organization:
                services.enforce_feature(organization, feature)

            return func(*args, **kwargs)
        return wrapper
    return decorator


def enforce_limit(metric: str) -> Callable:
    """
    Decorator to enforce plan limits before executing a function.

    Usage:
        @enforce_limit('workflows_count')
        def create_workflow(organization, name):
            ...

    Args:
        metric: Metric name to check (e.g., 'workflows_count')

    Raises:
        PlanLimitExceeded: If the limit is exceeded
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Try to find organization in args or kwargs
            organization = None

            # Check kwargs first
            if "organization" in kwargs:
                organization = kwargs["organization"]
            elif "org" in kwargs:
                organization = kwargs["org"]

            # Check args (look for Organization instances)
            if not organization:
                for arg in args:
                    if isinstance(arg, Organization):
                        organization = arg
                        break

            # Check if request object has active_org (from middleware)
            if not organization:
                for arg in args:
                    if hasattr(arg, "active_org"):
                        organization = arg.active_org
                        break

            if organization:
                services.enforce_limit(organization, metric)

            return func(*args, **kwargs)
        return wrapper
    return decorator


def check_and_increment(metric: str) -> Callable:
    """
    Decorator to check limit and increment usage after successful execution.

    This is useful for operations that create resources.

    Usage:
        @check_and_increment('workflows_count')
        def create_workflow(organization, name):
            workflow = Workflow.objects.create(...)
            return workflow

    Args:
        metric: Metric name to check and increment

    Raises:
        PlanLimitExceeded: If the limit is exceeded
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Try to find organization in args or kwargs
            organization = None

            # Check kwargs first
            if "organization" in kwargs:
                organization = kwargs["organization"]
            elif "org" in kwargs:
                organization = kwargs["org"]

            # Check args (look for Organization instances)
            if not organization:
                for arg in args:
                    if isinstance(arg, Organization):
                        organization = arg
                        break

            # Check if request object has active_org (from middleware)
            if not organization:
                for arg in args:
                    if hasattr(arg, "active_org"):
                        organization = arg.active_org
                        break

            # Enforce limit before execution
            if organization:
                services.enforce_limit(organization, metric)

            # Execute the function
            result = func(*args, **kwargs)

            # Increment usage after successful execution
            if organization:
                services.increment_usage(organization, metric)

            return result
        return wrapper
    return decorator
