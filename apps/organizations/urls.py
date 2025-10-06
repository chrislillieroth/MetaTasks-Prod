from django.urls import path
from django.http import HttpResponse

app_name = 'organizations'

def placeholder_view(request):
    return HttpResponse("Organizations module - Coming soon!")

urlpatterns = [
    path('', placeholder_view, name='list'),
    path('create/', placeholder_view, name='create'),
]