from django.urls import path
from django.http import HttpResponse, JsonResponse
from django.utils.timezone import now

def home(request):
    return HttpResponse("FAGNI API – OK", status=200)

def health(request):
    return JsonResponse({"ok": True, "time": now().isoformat()})

def favicon(_):
    # Répond vide pour éviter le 404 sur /favicon.ico
    return HttpResponse(status=204)

urlpatterns = [
    path("", home),                # accueil
    path("api/health/", health),   # health check
    path("favicon.ico", favicon),  # évite l'erreur favicon
]
