from django.urls import path
from django.http import HttpResponse

app_name = 'scheduling'

def placeholder_view(request):
    return HttpResponse("Scheduling module - Coming soon!")

urlpatterns = [
    path('', placeholder_view, name='calendar'),
    path('create/', placeholder_view, name='create'),
]