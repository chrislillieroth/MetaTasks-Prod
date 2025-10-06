"""
UI views for MetaTasks.
Following specification Section 31 for UX/UI patterns.
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator


@method_decorator(login_required, name='dispatch')
class DashboardView(TemplateView):
    """Main dashboard view."""
    template_name = 'ui/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add dashboard-specific context
        context['recent_workitems'] = []  # TODO: Fetch from service
        context['stats'] = {
            'total_workitems': 0,
            'active_workflows': 0,
            'team_members': 0,
        }
        return context


@method_decorator(login_required, name='dispatch')
class WorkflowListView(TemplateView):
    """List all workflows."""
    template_name = 'ui/workflows/list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['workflows'] = []  # TODO: Fetch from service
        return context


@method_decorator(login_required, name='dispatch')
class OrganizationListView(TemplateView):
    """List organizations."""
    template_name = 'ui/organizations/list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch organizations from user memberships
        context['organizations'] = self.request.user.memberships.select_related('organization').all()
        return context


@method_decorator(login_required, name='dispatch')
class SchedulingView(TemplateView):
    """Scheduling view."""
    template_name = 'ui/scheduling/index.html'


@method_decorator(login_required, name='dispatch')
class IntegrationsView(TemplateView):
    """Integrations view."""
    template_name = 'ui/integrations/index.html'


@method_decorator(login_required, name='dispatch')
class LicensingView(TemplateView):
    """Licensing view."""
    template_name = 'ui/licensing/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # TODO: Fetch licensing data from service
        context['current_plan'] = None
        context['usage'] = {}
        return context


@method_decorator(login_required, name='dispatch')
class AnalyticsView(TemplateView):
    """Analytics view."""
    template_name = 'ui/analytics/index.html'


@method_decorator(login_required, name='dispatch')
class AccountView(TemplateView):
    """User account view."""
    template_name = 'ui/accounts/profile.html'


@method_decorator(login_required, name='dispatch')
class SettingsView(TemplateView):
    """User settings view."""
    template_name = 'ui/accounts/settings.html'


def custom_404(request, exception=None):
    """Custom 404 error handler."""
    return render(request, 'ui/errors/404.html', status=404)


def custom_500(request):
    """Custom 500 error handler."""
    return render(request, 'ui/errors/500.html', status=500)
