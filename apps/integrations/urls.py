from django.urls import path
from django.http import HttpResponse

app_name = 'integrations'

def placeholder_view(request):
    return HttpResponse("Integrations module - Coming soon!")

urlpatterns = [
    path('', placeholder_view, name='list'),
    path('browse/', placeholder_view, name='browse'),
]