"""
Tests for licensing models, services, and decorators.
"""

import pytest
from django.contrib.auth import get_user_model

from apps.common.exceptions import FeatureNotAvailable, PlanLimitExceeded
from apps.licensing import decorators, selectors, services
from apps.licensing.models import Plan, Usage
from apps.organizations import services as org_services

User = get_user_model()


@pytest.fixture
def user(db):
    """Create a test user."""
    return User.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="testpass123",
    )


@pytest.fixture
def organization(user):
    """Create a test organization."""
    return org_services.create_organization(
        name="Test Organization",
        owner=user,
    )


@pytest.fixture
def free_plan(db):
    """Create a free plan."""
    return services.create_plan(
        name="Free Plan",
        plan_type=Plan.PlanType.FREE,
        max_users=5,
        max_workflows=10,
        max_work_items=100,
        max_storage_bytes=1024 * 1024 * 100,  # 100 MB
        has_api_access=True,
        has_integrations=False,
        has_advanced_workflows=False,
        has_priority_support=False,
    )


@pytest.fixture
def pro_plan(db):
    """Create a professional plan."""
    return services.create_plan(
        name="Professional Plan",
        plan_type=Plan.PlanType.PROFESSIONAL,
        max_users=0,  # Unlimited
        max_workflows=0,  # Unlimited
        max_work_items=0,  # Unlimited
        max_storage_bytes=0,  # Unlimited
        has_api_access=True,
        has_integrations=True,
        has_advanced_workflows=True,
        has_priority_support=True,
    )


@pytest.mark.django_db
class TestPlanModel:
    """Tests for the Plan model."""

    def test_create_plan(self, free_plan):
        """Test creating a plan."""
        assert free_plan.name == "Free Plan"
        assert free_plan.plan_type == Plan.PlanType.FREE
        assert free_plan.max_users == 5
        assert free_plan.has_api_access is True
        assert free_plan.has_integrations is False

    def test_plan_str(self, free_plan):
        """Test plan string representation."""
        assert str(free_plan) == "Free Plan"

    def test_is_unlimited(self, free_plan, pro_plan):
        """Test checking if a limit is unlimited."""
        assert free_plan.is_unlimited("max_users") is False
        assert pro_plan.is_unlimited("max_users") is True


@pytest.mark.django_db
class TestUsageModel:
    """Tests for the Usage model."""

    def test_create_usage(self, organization, free_plan):
        """Test creating usage record."""
        usage = Usage.objects.create(
            organization=organization,
            plan=free_plan,
        )
        assert usage.organization == organization
        assert usage.plan == free_plan
        assert usage.users_count == 0

    def test_usage_str(self, organization, free_plan):
        """Test usage string representation."""
        usage = Usage.objects.create(
            organization=organization,
            plan=free_plan,
        )
        assert str(usage) == "Test Organization - Free Plan"

    def test_is_over_limit(self, organization, free_plan):
        """Test checking if over limit."""
        usage = Usage.objects.create(
            organization=organization,
            plan=free_plan,
            users_count=5,
        )
        assert usage.is_over_limit("users_count") is True

        usage.users_count = 4
        usage.save()
        assert usage.is_over_limit("users_count") is False

    def test_is_over_limit_unlimited(self, organization, pro_plan):
        """Test that unlimited plans never hit limits."""
        usage = Usage.objects.create(
            organization=organization,
            plan=pro_plan,
            users_count=1000000,
        )
        assert usage.is_over_limit("users_count") is False

    def test_get_remaining(self, organization, free_plan):
        """Test getting remaining capacity."""
        usage = Usage.objects.create(
            organization=organization,
            plan=free_plan,
            users_count=3,
        )
        assert usage.get_remaining("users_count") == 2

    def test_get_remaining_unlimited(self, organization, pro_plan):
        """Test that unlimited plans return None for remaining."""
        usage = Usage.objects.create(
            organization=organization,
            plan=pro_plan,
            users_count=1000,
        )
        assert usage.get_remaining("users_count") is None


@pytest.mark.django_db
class TestLicensingServices:
    """Tests for licensing services."""

    def test_create_plan(self):
        """Test creating a plan via service."""
        plan = services.create_plan(
            name="Starter Plan",
            plan_type=Plan.PlanType.STARTER,
            max_users=10,
            max_workflows=20,
            max_work_items=200,
            max_storage_bytes=1024 * 1024 * 500,
            description="Starter plan for small teams",
            has_integrations=True,
        )
        assert plan.name == "Starter Plan"
        assert plan.has_integrations is True
        assert plan.has_advanced_workflows is False

    def test_assign_plan(self, organization, free_plan):
        """Test assigning a plan to an organization."""
        usage = services.assign_plan(organization, free_plan)
        assert usage.organization == organization
        assert usage.plan == free_plan

    def test_assign_plan_updates_existing(self, organization, free_plan, pro_plan):
        """Test that assigning a new plan updates existing usage."""
        usage1 = services.assign_plan(organization, free_plan)
        usage2 = services.assign_plan(organization, pro_plan)

        assert usage1.id == usage2.id
        assert usage2.plan == pro_plan

    def test_increment_usage(self, organization, free_plan):
        """Test incrementing usage metrics."""
        services.assign_plan(organization, free_plan)

        usage = services.increment_usage(organization, "users_count", 1)
        assert usage.users_count == 1

        usage = services.increment_usage(organization, "users_count", 2)
        assert usage.users_count == 3

    def test_increment_usage_invalid_metric(self, organization, free_plan):
        """Test that invalid metrics raise error."""
        services.assign_plan(organization, free_plan)

        with pytest.raises(ValueError):
            services.increment_usage(organization, "invalid_metric")

    def test_decrement_usage(self, organization, free_plan):
        """Test decrementing usage metrics."""
        usage = services.assign_plan(organization, free_plan)
        usage.users_count = 5
        usage.save()

        usage = services.decrement_usage(organization, "users_count", 2)
        assert usage.users_count == 3

    def test_decrement_usage_not_below_zero(self, organization, free_plan):
        """Test that decrement doesn't go below zero."""
        usage = services.assign_plan(organization, free_plan)
        usage.users_count = 2
        usage.save()

        usage = services.decrement_usage(organization, "users_count", 5)
        assert usage.users_count == 0

    def test_check_limit(self, organization, free_plan):
        """Test checking if at limit."""
        usage = services.assign_plan(organization, free_plan)

        assert services.check_limit(organization, "users_count") is False

        usage.users_count = 5
        usage.save()

        assert services.check_limit(organization, "users_count") is True

    def test_enforce_limit_passes(self, organization, free_plan):
        """Test that enforce_limit passes when under limit."""
        services.assign_plan(organization, free_plan)

        # Should not raise
        services.enforce_limit(organization, "users_count")

    def test_enforce_limit_raises(self, organization, free_plan):
        """Test that enforce_limit raises when over limit."""
        usage = services.assign_plan(organization, free_plan)
        usage.users_count = 5
        usage.save()

        with pytest.raises(PlanLimitExceeded) as exc_info:
            services.enforce_limit(organization, "users_count")

        assert exc_info.value.metric == "users_count"
        assert exc_info.value.limit == 5

    def test_check_feature(self, organization, free_plan):
        """Test checking feature availability."""
        services.assign_plan(organization, free_plan)

        assert services.check_feature(organization, "has_api_access") is True
        assert services.check_feature(organization, "has_integrations") is False

    def test_enforce_feature_passes(self, organization, free_plan):
        """Test that enforce_feature passes when feature available."""
        services.assign_plan(organization, free_plan)

        # Should not raise
        services.enforce_feature(organization, "has_api_access")

    def test_enforce_feature_raises(self, organization, free_plan):
        """Test that enforce_feature raises when feature unavailable."""
        services.assign_plan(organization, free_plan)

        with pytest.raises(FeatureNotAvailable) as exc_info:
            services.enforce_feature(organization, "has_integrations")

        assert exc_info.value.feature == "has_integrations"
        assert exc_info.value.plan_name == "Free Plan"


@pytest.mark.django_db
class TestLicensingSelectors:
    """Tests for licensing selectors."""

    def test_get_organization_usage(self, organization, free_plan):
        """Test getting organization usage."""
        services.assign_plan(organization, free_plan)

        usage = selectors.get_organization_usage(organization)
        assert usage is not None
        assert usage.organization == organization

    def test_get_organization_usage_not_found(self, organization):
        """Test getting usage when not assigned."""
        usage = selectors.get_organization_usage(organization)
        assert usage is None

    def test_get_organization_plan(self, organization, free_plan):
        """Test getting organization plan."""
        services.assign_plan(organization, free_plan)

        plan = selectors.get_organization_plan(organization)
        assert plan == free_plan

    def test_get_organization_plan_not_found(self, organization):
        """Test getting plan when not assigned."""
        plan = selectors.get_organization_plan(organization)
        assert plan is None

    def test_get_active_plans(self, free_plan, pro_plan):
        """Test getting active plans."""
        plans = selectors.get_active_plans()
        assert plans.count() == 2
        assert free_plan in plans
        assert pro_plan in plans

    def test_get_plan_by_type(self, free_plan, pro_plan):
        """Test getting plan by type."""
        plan = selectors.get_plan_by_type(Plan.PlanType.FREE)
        assert plan == free_plan

        plan = selectors.get_plan_by_type(Plan.PlanType.PROFESSIONAL)
        assert plan == pro_plan

    def test_get_usage_stats(self, organization, free_plan):
        """Test getting usage statistics."""
        usage = services.assign_plan(organization, free_plan)
        usage.users_count = 3
        usage.workflows_count = 5
        usage.save()

        stats = selectors.get_usage_stats(organization)

        assert stats["users_count"] == 3
        assert stats["workflows_count"] == 5
        assert stats["users_remaining"] == 2
        assert stats["workflows_remaining"] == 5

    def test_get_usage_stats_unlimited(self, organization, pro_plan):
        """Test getting stats for unlimited plan."""
        usage = services.assign_plan(organization, pro_plan)
        usage.users_count = 1000
        usage.save()

        stats = selectors.get_usage_stats(organization)

        assert stats["users_count"] == 1000
        assert stats["users_remaining"] is None


@pytest.mark.django_db
class TestLicensingDecorators:
    """Tests for licensing decorators."""

    def test_require_feature_passes(self, organization, free_plan):
        """Test require_feature decorator when feature available."""
        services.assign_plan(organization, free_plan)

        @decorators.require_feature("has_api_access")
        def test_function(organization):
            return "success"

        result = test_function(organization)
        assert result == "success"

    def test_require_feature_raises(self, organization, free_plan):
        """Test require_feature decorator when feature unavailable."""
        services.assign_plan(organization, free_plan)

        @decorators.require_feature("has_integrations")
        def test_function(organization):
            return "success"

        with pytest.raises(FeatureNotAvailable):
            test_function(organization)

    def test_enforce_limit_decorator_passes(self, organization, free_plan):
        """Test enforce_limit decorator when under limit."""
        services.assign_plan(organization, free_plan)

        @decorators.enforce_limit("users_count")
        def test_function(organization):
            return "success"

        result = test_function(organization)
        assert result == "success"

    def test_enforce_limit_decorator_raises(self, organization, free_plan):
        """Test enforce_limit decorator when over limit."""
        usage = services.assign_plan(organization, free_plan)
        usage.users_count = 5
        usage.save()

        @decorators.enforce_limit("users_count")
        def test_function(organization):
            return "success"

        with pytest.raises(PlanLimitExceeded):
            test_function(organization)

    def test_check_and_increment_decorator(self, organization, free_plan):
        """Test check_and_increment decorator."""
        services.assign_plan(organization, free_plan)

        @decorators.check_and_increment("workflows_count")
        def test_function(organization):
            return "success"

        # Initial count should be 0
        usage = Usage.objects.get(organization=organization)
        assert usage.workflows_count == 0

        # Call the decorated function
        result = test_function(organization)
        assert result == "success"

        # Count should be incremented
        usage.refresh_from_db()
        assert usage.workflows_count == 1

    def test_check_and_increment_raises_at_limit(self, organization, free_plan):
        """Test check_and_increment decorator raises when at limit."""
        usage = services.assign_plan(organization, free_plan)
        usage.workflows_count = 10  # At the limit
        usage.save()

        @decorators.check_and_increment("workflows_count")
        def test_function(organization):
            return "success"

        with pytest.raises(PlanLimitExceeded):
            test_function(organization)

        # Count should not have incremented
        usage.refresh_from_db()
        assert usage.workflows_count == 10


@pytest.mark.django_db
class TestLicensingIntegration:
    """Integration tests for licensing system."""

    def test_complete_licensing_workflow(self, organization, free_plan):
        """Test a complete licensing workflow."""
        # Assign plan
        usage = services.assign_plan(organization, free_plan)
        assert usage.plan == free_plan

        # Check limits
        assert services.check_limit(organization, "users_count") is False

        # Increment usage
        for _ in range(4):
            services.increment_usage(organization, "users_count")

        usage.refresh_from_db()
        assert usage.users_count == 4

        # Still under limit
        assert services.check_limit(organization, "users_count") is False

        # One more increment
        services.increment_usage(organization, "users_count")

        # Now at limit
        assert services.check_limit(organization, "users_count") is True

        # Should raise on enforce
        with pytest.raises(PlanLimitExceeded):
            services.enforce_limit(organization, "users_count")

    def test_upgrade_plan_scenario(self, organization, free_plan, pro_plan):
        """Test upgrading from free to pro plan."""
        # Start with free plan
        usage = services.assign_plan(organization, free_plan)
        usage.users_count = 5
        usage.save()

        # At limit on free plan
        assert services.check_limit(organization, "users_count") is True

        # Upgrade to pro plan
        services.assign_plan(organization, pro_plan)

        # No longer at limit (unlimited)
        assert services.check_limit(organization, "users_count") is False

        # Can increment without limit
        services.increment_usage(organization, "users_count", 1000)

        # Refresh to get updated usage with new plan
        usage = Usage.objects.get(organization=organization)
        assert usage.users_count == 1005  # 5 (initial) + 1000 (increment)
