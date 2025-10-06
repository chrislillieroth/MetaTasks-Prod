from django.urls import path
from django.http import HttpResponse

app_name = 'audit'

def placeholder_view(request):
    return HttpResponse("Audit module - Coming soon!")

urlpatterns = [
    path('activity/', placeholder_view, name='activity'),
]