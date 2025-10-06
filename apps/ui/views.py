from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from django.urls import reverse


def dashboard(request):
    """Main dashboard view with overview stats and recent activity."""
    
    # Mock stats for now until models are implemented
    stats = {
        'active_workflows': 24,
        'organizations': 8,
        'scheduled_tasks': 156,
        'integrations': 12,
    }
    
    # Mock recent activities
    recent_activities = [
        {
            'type': 'workflow_completed',
            'title': 'Data Processing Pipeline',
            'description': 'completed successfully',
            'timestamp': timezone.now(),
            'status': 'success'
        },
        {
            'type': 'workflow_created',
            'title': 'Email Campaign Automation',
            'description': 'created',
            'timestamp': timezone.now(),
            'status': 'info'
        },
        {
            'type': 'integration_warning',
            'title': 'Slack Notifications',
            'description': 'needs attention',
            'timestamp': timezone.now(),
            'status': 'warning'
        }
    ]
    
    # Mock upcoming tasks
    upcoming_tasks = [
        {
            'name': 'Review monthly reports',
            'due_date': timezone.now() + timezone.timedelta(hours=2),
            'priority': 'high'
        },
        {
            'name': 'Update client workflow',
            'due_date': timezone.now() + timezone.timedelta(days=1),
            'priority': 'medium'
        },
        {
            'name': 'Team sync meeting',
            'due_date': timezone.now() + timezone.timedelta(days=3),
            'priority': 'low'
        }
    ]
    
    context = {
        'stats': stats,
        'recent_activities': recent_activities,
        'upcoming_tasks': upcoming_tasks,
    }
    
    return render(request, 'ui/dashboard.html', context)


def search(request):
    """Global search across all entities."""
    query = request.GET.get('q', '').strip()
    
    # Mock search results for now
    results = {
        'workflows': [],
        'organizations': [],
        'tasks': [],
    }
    
    if query:
        # Mock some search results
        if 'data' in query.lower():
            results['workflows'].append({
                'name': 'Data Processing Pipeline',
                'description': 'Automated data processing workflow'
            })
        if 'team' in query.lower():
            results['organizations'].append({
                'name': 'Team Alpha',
                'description': 'Primary development team'
            })
    
    total_results = sum(len(v) for v in results.values())
    
    context = {
        'query': query,
        'results': results,
        'total_results': total_results,
    }
    
    return render(request, 'ui/search_results.html', context)


@require_http_methods(["GET"])
def notifications_api(request):
    """API endpoint for fetching notifications."""
    # Mock notifications data
    notifications = [
        {
            'id': 1,
            'title': 'Workflow completed',
            'message': 'Data Processing Pipeline completed successfully',
            'type': 'success',
            'created_at': timezone.now().isoformat(),
            'read': False,
        },
        {
            'id': 2,
            'title': 'New organization member',
            'message': 'John Doe joined your organization',
            'type': 'info',
            'created_at': timezone.now().isoformat(),
            'read': False,
        },
        {
            'id': 3,
            'title': 'Integration warning',
            'message': 'Slack integration needs attention',
            'type': 'warning',
            'created_at': timezone.now().isoformat(),
            'read': True,
        },
    ]
    
    # Filter unread for count
    unread_count = sum(1 for n in notifications if not n['read'])
    
    return JsonResponse({
        'results': notifications,
        'unread_count': unread_count,
    })


def profile(request):
    """User profile page."""
    # Create a mock user for demo purposes
    mock_user = {
        'first_name': 'John',
        'last_name': 'Doe',
        'username': 'johndoe',
        'email': 'john.doe@example.com',
        'date_joined': timezone.now() - timezone.timedelta(days=30),
        'last_login': timezone.now() - timezone.timedelta(hours=2),
    }
    
    return render(request, 'ui/profile.html', {
        'user': mock_user,
    })


def settings(request):
    """User settings page."""
    # Create a mock user for demo purposes
    mock_user = {
        'first_name': 'John',
        'last_name': 'Doe',
        'username': 'johndoe',
        'email': 'john.doe@example.com',
    }
    
    return render(request, 'ui/settings.html', {
        'user': mock_user,
    })


def health_check(request):
    """Health check endpoint for monitoring."""
    return JsonResponse({
        'status': 'healthy',
        'timestamp': timezone.now().isoformat(),
        'version': '0.1.0',
    })