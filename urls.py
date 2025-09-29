from django.urls import path
from django.http import HttpResponse, JsonResponse
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
import json

# ===== Stockage en mémoire (reset à chaque redeploy) =====
ORDERS = []
CLIENTS = []
PARTNERS = []
PAYMENTS = []
INCIDENTS = []

NEXT_ID = {
    "order": 1,
    "client": 1,
    "partner": 1,
    "payment": 1,
    "incident": 1,
}

# ===== Utilitaires =====
def add_cors(resp):
    resp["Access-Control-Allow-Origin"] = "*"
    resp["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    resp["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return resp

def parse_json(request):
    try:
        body = request.body.decode("utf-8") if request.body else "{}"
        return json.loads(body)
    except Exception:
        return None

def home(request):
    return add_cors(HttpResponse("FAGNI API – OK", status=200))

def health(request):
    return add_cors(JsonResponse({"ok": True, "time": now().isoformat()}))

def favicon(_):
    return add_cors(HttpResponse(status=204))

# ===== Handlers génériques (GET liste / POST création) =====
def make_list_handler(store_key, store):
    @csrf_exempt
    def handler(request):
        if request.method == "OPTIONS":
            return add_cors(HttpResponse(status=204))

        if request.method == "GET":
            return add_cors(JsonResponse({"ok": True, "data": store}, safe=False))

        if request.method == "POST":
            payload = parse_json(request)
            if payload is None:
                return add_cors(JsonResponse({"error": "Invalid JSON"}, status=400))
            # assigne un ID
            payload["id"] = NEXT_ID[store_key]
            NEXT_ID[store_key] += 1
            # timestamp simple
            payload.setdefault("created_at", now().isoformat())
            store.append(payload)
            return add_cors(JsonResponse({"ok": True, "data": payload}, status=201))

        return add_cors(JsonResponse({"error": "Method not allowed"}, status=405))
    return handler

orders = make_list_handler("order", ORDERS)
clients = make_list_handler("client", CLIENTS)
partners = make_list_handler("partner", PARTNERS)
payments = make_list_handler("payment", PAYMENTS)
incidents = make_list_handler("incident", INCIDENTS)

# ===== Routes =====
urlpatterns = [
    path("", home),
    path("api/health/", health),

    path("api/orders/", orders),
    path("api/clients/", clients),
    path("api/partners/", partners),
    path("api/payments/", payments),
    path("api/incidents/", incidents),

    path("favicon.ico", favicon),
]
