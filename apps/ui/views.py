"""
UI views for MetaTasks.
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def dashboard(request):
    """Dashboard view with overview statistics."""
    context = {
        'stats': {
            'total_workflows': 12,
            'active_items': 34,
            'completed_today': 8,
            'team_members': 5,
        },
        'recent_items': [
            {'id': 1, 'title': 'Design Review', 'status': 'In Progress', 'assignee': 'John Doe'},
            {'id': 2, 'title': 'API Integration', 'status': 'Pending', 'assignee': 'Jane Smith'},
            {'id': 3, 'title': 'Bug Fix #234', 'status': 'Completed', 'assignee': 'Bob Johnson'},
        ],
    }
    return render(request, 'ui/dashboard/index.html', context)


@login_required
def workflows(request):
    """Workflows list view."""
    context = {
        'workflows': [
            {'id': 1, 'name': 'Development Workflow', 'items': 15, 'status': 'Active'},
            {'id': 2, 'name': 'Design Review', 'items': 8, 'status': 'Active'},
            {'id': 3, 'name': 'QA Testing', 'items': 12, 'status': 'Active'},
        ],
    }
    return render(request, 'ui/workflows/list.html', context)


@login_required
def work_items(request):
    """Work items list view."""
    context = {
        'work_items': [
            {'id': 1, 'title': 'Implement user authentication', 'workflow': 'Development', 'status': 'In Progress', 'priority': 'High'},
            {'id': 2, 'title': 'Design dashboard mockups', 'workflow': 'Design', 'status': 'Pending', 'priority': 'Medium'},
            {'id': 3, 'title': 'Write API documentation', 'workflow': 'Development', 'status': 'Completed', 'priority': 'Low'},
        ],
    }
    return render(request, 'ui/workflows/items.html', context)


@login_required
def scheduling(request):
    """Scheduling calendar view."""
    return render(request, 'ui/dashboard/scheduling.html')


@login_required
def profile(request):
    """User profile view."""
    return render(request, 'ui/settings/profile.html')


@login_required
def settings(request):
    """Settings view."""
    return render(request, 'ui/settings/index.html')


@login_required
def search(request):
    """Search results view."""
    query = request.GET.get('q', '')
    context = {
        'query': query,
        'results': [] if not query else [
            {'type': 'workflow', 'title': 'Development Workflow', 'description': 'Main development process'},
            {'type': 'item', 'title': 'Bug Fix #234', 'description': 'Fix authentication issue'},
        ],
    }
    return render(request, 'ui/dashboard/search.html', context)
