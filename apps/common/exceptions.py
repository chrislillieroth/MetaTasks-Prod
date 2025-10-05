"""
Common exceptions for MetaTasks.
"""


class MetaTasksException(Exception):
    """Base exception for all MetaTasks custom exceptions."""

    pass


class LicenseException(MetaTasksException):
    """Base exception for licensing-related errors."""

    pass


class PlanLimitExceeded(LicenseException):
    """Raised when attempting to exceed a plan's limits."""

    def __init__(self, metric: str, limit: int, current: int):
        self.metric = metric
        self.limit = limit
        self.current = current
        super().__init__(
            f"Plan limit exceeded for {metric}: {current}/{limit}"
        )


class FeatureNotAvailable(LicenseException):
    """Raised when attempting to use a feature not in the current plan."""

    def __init__(self, feature: str, plan_name: str):
        self.feature = feature
        self.plan_name = plan_name
        super().__init__(
            f"Feature '{feature}' is not available in plan '{plan_name}'"
        )
