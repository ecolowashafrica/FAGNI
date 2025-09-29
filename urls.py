from django.urls import path
from django.http import JsonResponse
from django.utils.timezone import now

def health(request):
    return JsonResponse({'ok': True, 'time': now().isoformat()})

urlpatterns = [
    path('api/health/', health),
]
