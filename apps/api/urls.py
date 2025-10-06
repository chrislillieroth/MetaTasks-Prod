from django.urls import path
from django.http import JsonResponse

app_name = 'api'

def placeholder_api(request):
    return JsonResponse({'message': 'API module - Coming soon!'})

urlpatterns = [
    path('', placeholder_api, name='root'),
]