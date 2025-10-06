from django.urls import path
from django.http import HttpResponse

app_name = 'workflows'

def placeholder_view(request):
    return HttpResponse("Workflows module - Coming soon!")

urlpatterns = [
    path('', placeholder_view, name='list'),
    path('create/', placeholder_view, name='create'),
    path('templates/', placeholder_view, name='templates'),
]