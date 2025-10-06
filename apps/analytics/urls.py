from django.urls import path
from django.http import HttpResponse

app_name = 'analytics'

def placeholder_view(request):
    return HttpResponse("Analytics module - Coming soon!")

urlpatterns = [
    path('', placeholder_view, name='dashboard'),
]