from django.urls import path
from django.http import HttpResponse

app_name = 'billing'

def placeholder_view(request):
    return HttpResponse("Billing module - Coming soon!")

urlpatterns = [
    path('subscription/', placeholder_view, name='subscription'),
]