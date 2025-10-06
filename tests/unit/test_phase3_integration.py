"""
Integration test demonstrating Phase 3 licensing enforcement.

This test demonstrates the complete licensing workflow including:
- Creating plans with different limits
- Assigning plans to organizations
- Enforcing limits through decorators
- Checking feature availability
"""

import pytest
from django.contrib.auth import get_user_model

from apps.common.exceptions import FeatureNotAvailable, PlanLimitExceeded
from apps.licensing import decorators, selectors, services
from apps.licensing.models import Plan
from apps.organizations import services as org_services

User = get_user_model()


@pytest.mark.django_db
class TestPhase3Integration:
    """Integration tests demonstrating Phase 3 success criteria."""

    def test_guard_denies_over_limit(self):
        """Test that guard decorator denies actions when over limit."""
        # Setup
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
        )
        organization = org_services.create_organization(
            name="Test Corp",
            owner=user,
        )

        # Create a plan with strict limits
        plan = services.create_plan(
            name="Strict Plan",
            plan_type=Plan.PlanType.STARTER,
            max_users=2,
            max_workflows=3,
            max_work_items=10,
            max_storage_bytes=1024 * 1024,  # 1 MB
            has_api_access=True,
            has_integrations=False,
        )
        services.assign_plan(organization, plan)

        # Create a function that uses the enforce_limit decorator
        @decorators.enforce_limit("workflows_count")
        def create_workflow(org, name):
            return f"Created workflow: {name}"

        # Should work when under limit
        result = create_workflow(organization, "Workflow 1")
        assert result == "Created workflow: Workflow 1"

        # Increment usage to the limit
        services.increment_usage(organization, "workflows_count", 3)

        # Should now deny the action
        with pytest.raises(PlanLimitExceeded) as exc_info:
            create_workflow(organization, "Workflow 4")

        assert exc_info.value.metric == "workflows_count"
        assert exc_info.value.limit == 3
        assert exc_info.value.current == 3

    def test_feature_guard_denies_unavailable_features(self):
        """Test that feature guard denies access to unavailable features."""
        # Setup
        user = User.objects.create_user(
            username="testuser2",
            email="test2@example.com",
            password="testpass123",
        )
        organization = org_services.create_organization(
            name="Small Business",
            owner=user,
        )

        # Create a free plan without integrations
        free_plan = services.create_plan(
            name="Free Tier",
            plan_type=Plan.PlanType.FREE,
            max_users=5,
            max_workflows=10,
            max_work_items=100,
            max_storage_bytes=10 * 1024 * 1024,  # 10 MB
            has_api_access=True,
            has_integrations=False,  # No integrations!
        )
        services.assign_plan(organization, free_plan)

        # Create a function that requires integrations feature
        @decorators.require_feature("has_integrations")
        def setup_integration(org, integration_type):
            return f"Setting up {integration_type}"

        # Should deny access to integrations
        with pytest.raises(FeatureNotAvailable) as exc_info:
            setup_integration(organization, "Slack")

        assert exc_info.value.feature == "has_integrations"
        assert exc_info.value.plan_name == "Free Tier"

        # Upgrade to professional plan with integrations
        pro_plan = services.create_plan(
            name="Professional",
            plan_type=Plan.PlanType.PROFESSIONAL,
            max_users=0,  # Unlimited
            max_workflows=0,  # Unlimited
            max_work_items=0,  # Unlimited
            max_storage_bytes=0,  # Unlimited
            has_api_access=True,
            has_integrations=True,  # Now has integrations!
        )
        services.assign_plan(organization, pro_plan)

        # Should now allow access
        result = setup_integration(organization, "Slack")
        assert result == "Setting up Slack"

    def test_complete_licensing_workflow_with_usage_tracking(self):
        """Test complete workflow: assign plan, track usage, enforce limits."""
        # Setup
        user = User.objects.create_user(
            username="testuser3",
            email="test3@example.com",
            password="testpass123",
        )
        organization = org_services.create_organization(
            name="Growing Startup",
            owner=user,
        )

        # Start with starter plan
        starter = services.create_plan(
            name="Starter",
            plan_type=Plan.PlanType.STARTER,
            max_users=10,
            max_workflows=25,
            max_work_items=500,
            max_storage_bytes=100 * 1024 * 1024,  # 100 MB
            has_api_access=True,
            has_integrations=True,
        )
        services.assign_plan(organization, starter)

        # Check initial usage
        stats = selectors.get_usage_stats(organization)
        assert stats["users_count"] == 0
        assert stats["users_remaining"] == 10

        # Simulate adding users
        for _i in range(8):
            services.increment_usage(organization, "users_count")

        # Check updated usage
        stats = selectors.get_usage_stats(organization)
        assert stats["users_count"] == 8
        assert stats["users_remaining"] == 2

        # Not at limit yet
        assert not services.check_limit(organization, "users_count")

        # Add 2 more users to reach limit
        services.increment_usage(organization, "users_count", 2)

        # Now at limit
        assert services.check_limit(organization, "users_count")

        # Should block further additions
        with pytest.raises(PlanLimitExceeded):
            services.enforce_limit(organization, "users_count")

        # Upgrade to enterprise (unlimited)
        enterprise = services.create_plan(
            name="Enterprise",
            plan_type=Plan.PlanType.ENTERPRISE,
            max_users=0,  # Unlimited
            max_workflows=0,  # Unlimited
            max_work_items=0,  # Unlimited
            max_storage_bytes=0,  # Unlimited
            has_api_access=True,
            has_integrations=True,
            has_advanced_workflows=True,
            has_priority_support=True,
        )
        services.assign_plan(organization, enterprise)

        # No longer at limit (unlimited)
        assert not services.check_limit(organization, "users_count")

        # Can add more users
        services.increment_usage(organization, "users_count", 100)

        # Still no limit
        assert not services.check_limit(organization, "users_count")

        # Check final stats show unlimited
        stats = selectors.get_usage_stats(organization)
        assert stats["users_count"] == 110  # 10 + 100
        assert stats["users_remaining"] is None  # Unlimited!
