"""
Licensing models for MetaTasks.
"""

from django.core.validators import MinValueValidator
from django.db import models


class Plan(models.Model):
    """Subscription plan defining limits and features."""

    class PlanType(models.TextChoices):
        FREE = "free", "Free"
        STARTER = "starter", "Starter"
        PROFESSIONAL = "professional", "Professional"
        ENTERPRISE = "enterprise", "Enterprise"

    name = models.CharField(max_length=100, unique=True)
    plan_type = models.CharField(
        max_length=20,
        choices=PlanType.choices,
        default=PlanType.FREE,
    )
    description = models.TextField(blank=True)

    # Limits
    max_users = models.IntegerField(
        validators=[MinValueValidator(0)],
        help_text="Maximum number of users (0 = unlimited)",
    )
    max_workflows = models.IntegerField(
        validators=[MinValueValidator(0)],
        help_text="Maximum number of workflows (0 = unlimited)",
    )
    max_work_items = models.IntegerField(
        validators=[MinValueValidator(0)],
        help_text="Maximum number of work items (0 = unlimited)",
    )
    max_storage_bytes = models.BigIntegerField(
        validators=[MinValueValidator(0)],
        help_text="Maximum storage in bytes (0 = unlimited)",
    )

    # Features
    has_api_access = models.BooleanField(default=True)
    has_integrations = models.BooleanField(default=False)
    has_advanced_workflows = models.BooleanField(default=False)
    has_priority_support = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def is_unlimited(self, limit_field: str) -> bool:
        """Check if a specific limit is unlimited (0)."""
        return getattr(self, limit_field, 1) == 0


class Usage(models.Model):
    """Track organization usage metrics for licensing enforcement."""

    organization = models.OneToOneField(
        "organizations.Organization",
        on_delete=models.CASCADE,
        related_name="usage",
    )
    plan = models.ForeignKey(
        Plan,
        on_delete=models.PROTECT,
        related_name="usages",
    )

    # Usage counters
    users_count = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
    )
    workflows_count = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
    )
    work_items_count = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
    )
    storage_bytes = models.BigIntegerField(
        default=0,
        validators=[MinValueValidator(0)],
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Usages"

    def __str__(self):
        return f"{self.organization.name} - {self.plan.name}"

    def is_over_limit(self, metric: str) -> bool:
        """Check if a specific metric is at or over the plan limit."""
        # Convert metric name to limit field name
        # E.g., "users_count" -> "max_users", "storage_bytes" -> "max_storage_bytes"
        if metric.endswith("_count"):
            limit_field = f"max_{metric[:-6]}"  # Remove "_count" and add "max_"
        else:
            limit_field = f"max_{metric}"

        if not hasattr(self.plan, limit_field):
            return False

        limit = getattr(self.plan, limit_field)
        # 0 means unlimited
        if limit == 0:
            return False

        current = getattr(self, metric, 0)
        return current >= limit

    def get_remaining(self, metric: str) -> int | None:
        """Get remaining capacity for a metric. None if unlimited."""
        # Convert metric name to limit field name
        # E.g., "users_count" -> "max_users", "storage_bytes" -> "max_storage_bytes"
        if metric.endswith("_count"):
            limit_field = f"max_{metric[:-6]}"  # Remove "_count" and add "max_"
        else:
            limit_field = f"max_{metric}"

        if not hasattr(self.plan, limit_field):
            return None

        limit = getattr(self.plan, limit_field)
        # 0 means unlimited
        if limit == 0:
            return None

        current = getattr(self, metric, 0)
        return max(0, limit - current)
