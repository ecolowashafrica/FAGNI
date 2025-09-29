from django.urls import path
from django.http import HttpResponse, JsonResponse
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
import json

# Stockage temporaire en mémoire (reset à chaque redéploiement)
ORDERS = []
NEXT_ID = 1

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
def orders(request):
    global NEXT_ID
    if request.method == "OPTIONS":
        return add_cors(HttpResponse(status=204))

    if request.method == "GET":
        # Retourner la liste des commandes
        return add_cors(JsonResponse({"ok": True, "orders": ORDERS}, safe=False))

    if request.method == "POST":
        try:
            body = request.body.decode("utf-8") if request.body else "{}"
            data = json.loads(body)
        except Exception:
            return add_cors(JsonResponse({"error": "Invalid JSON"}, status=400))

        # Générer un nouvel ID et stocker
        data["id"] = NEXT_ID
        NEXT_ID += 1
        ORDERS.append(data)

        return add_cors(JsonResponse({"ok": True, "order": data}, status=201))

    return add_cors(JsonResponse({"error": "Method not allowed"}, status=405))

# Routes
urlpatterns = [
    path("", home),
    path("api/health/", health),
    path("api/orders/", orders),
    path("favicon.ico", favicon),
]
