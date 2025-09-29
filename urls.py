from django.urls import path
from django.http import HttpResponse, JsonResponse
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
import json

# Ajout des en-têtes CORS
def add_cors(resp):
    resp["Access-Control-Allow-Origin"] = "*"
    resp["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    resp["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return resp

# Page d’accueil
def home(request):
    return add_cors(HttpResponse("FAGNI API – OK", status=200))

# Health check
def health(request):
    return add_cors(JsonResponse({"ok": True, "time": now().isoformat()}))

# Favicon (évite les erreurs 404)
def favicon(_):
    return add_cors(HttpResponse(status=204))

# Endpoint commandes
@csrf_exempt
def create_order(request):
    if request.method == "OPTIONS":
        return add_cors(HttpResponse(status=204))
    if request.method != "POST":
        return add_cors(JsonResponse({"error": "POST only"}, status=405))
    try:
        body = request.body.decode("utf-8") if request.body else "{}"
        data = json.loads(body)
    except Exception:
        return add_cors(JsonResponse({"error": "Invalid JSON"}, status=400))
    return add_cors(JsonResponse({"ok": True, "id": 1, "received": data}, status=201))

# Routes
urlpatterns = [
    path("", home),
    path("api/health/", health),
    path("api/orders/", create_order),
    path("favicon.ico", favicon),
]
