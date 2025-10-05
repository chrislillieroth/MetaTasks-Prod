"""
Common middleware for MetaTasks.
"""


from django.http import HttpRequest

from apps.organizations.models import Organization
from apps.organizations.selectors import get_user_default_organization


class ActiveOrganizationMiddleware:
    """
    Middleware to attach the active organization to the request.

    The active organization is determined by:
    1. Session key 'active_organization_id'
    2. Header 'X-Organization-ID'
    3. User's default organization (first membership)
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        request.active_org = self._get_active_organization(request)
        response = self.get_response(request)
        return response

    def _get_active_organization(self, request: HttpRequest) -> Organization | None:
        """
        Determine the active organization for the request.

        Args:
            request: Current HTTP request

        Returns:
            Organization instance or None
        """
        if (
            not hasattr(request, "user")
            or request.user is None
            or not request.user.is_authenticated
        ):
            return None

        # Try to get from session
        org_id = request.session.get("active_organization_id")
        if org_id:
            try:
                org = Organization.objects.get(id=org_id, is_active=True)
                # Verify user has access
                if org.memberships.filter(user=request.user, is_active=True).exists():
                    return org
            except Organization.DoesNotExist:
                # Clear invalid session data
                request.session.pop("active_organization_id", None)

        # Try to get from header
        org_id = request.headers.get("X-Organization-ID")
        if org_id:
            try:
                org = Organization.objects.get(id=org_id, is_active=True)
                # Verify user has access
                if org.memberships.filter(user=request.user, is_active=True).exists():
                    return org
            except (Organization.DoesNotExist, ValueError):
                pass

        # Fall back to user's default organization
        return get_user_default_organization(request.user)
