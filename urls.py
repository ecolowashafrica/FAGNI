from django.urls import path
from django.http import HttpResponse, JsonResponse
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
import json

# Page d’accueil
def home(request):
    return HttpResponse("FAGNI API – OK", status=200)

# Health check
def health(request):
    return JsonResponse({"ok": True, "time": now().isoformat()})

# Favicon (évite l’erreur 404)
def favicon(_):
    return HttpResponse(status=204)

# 👇 Nouvelle route pour simuler une commande
@csrf_exempt
def create_order(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)
    try:
        data = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    # Pour l’instant, pas de base → on simule un ID
    return JsonResponse({"ok": True, "id": 1, "received": data}, status=201)

# Liste des routes
urlpatterns = [
    path("", home),                     # /
    path("api/health/", health),        # /api/health/
    path("api/orders/", create_order),  # /api/orders/
    path("favicon.ico", favicon),       # /favicon.ico
]
