from django.urls import path
from django.http import HttpResponse

app_name = 'accounts'

def placeholder_view(request):
    return HttpResponse("Accounts module - Coming soon!")

urlpatterns = [
    path('profile/', placeholder_view, name='profile'),
    path('settings/', placeholder_view, name='settings'),
    path('logout/', placeholder_view, name='logout'),
]