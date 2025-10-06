from django.urls import path
from django.http import HttpResponse

app_name = 'notifications'

def placeholder_view(request):
    return HttpResponse("Notifications module - Coming soon!")

urlpatterns = [
    path('', placeholder_view, name='list'),
    path('all/', placeholder_view, name='all'),
]