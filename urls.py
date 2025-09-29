from django.urls import path
from django.http import HttpResponse, JsonResponse
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
import json

# ===== Stockage en mémoire (reset à chaque redeploy) =====
ORDERS, CLIENTS, PARTNERS, PAYMENTS, INCIDENTS = [], [], [], [], []
NEXT_ID = {"order": 1, "client": 1, "partner": 1, "payment": 1, "incident": 1}

# ===== Workflow des commandes =====
ORDER_STATUSES = [
    "PENDING_PAYMENT",
    "PAID",
    "COLLECTING",
    "PROCESSING",
    "READY",
    "DELIVERING",
    "DELIVERED",
]
NEXT_STATUS = {
    "PENDING_PAYMENT": "PAID",
    "PAID": "COLLECTING",
    "COLLECTING": "PROCESSING",
    "PROCESSING": "READY",
    "READY": "DELIVERING",
    "DELIVERING": "DELIVERED",
}

# ===== Utils =====
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

def find_order(oid):
    for o in ORDERS:
        if o.get("id") == oid:
            return o
    return None

# ===== Pages simples =====
def home(request):
    return add_cors(HttpResponse("FAGNI API – OK", status=200))

def health(request):
    return add_cors(JsonResponse({"ok": True, "time": now().isoformat()}))

def favicon(_):
    return add_cors(HttpResponse(status=204))

# ===== Fabrique de handlers (GET liste / POST création) =====
def make_list_handler(store_key, store, defaults=None):
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
            payload["id"] = NEXT_ID[store_key]
            NEXT_ID[store_key] += 1
            payload.setdefault("created_at", now().isoformat())
            if defaults:
                for k, v in defaults.items():
                    payload.setdefault(k, v)
            store.append(payload)
            return add_cors(JsonResponse({"ok": True, "data": payload}, status=201))

        return add_cors(JsonResponse({"error": "Method not allowed"}, status=405))
    return handler

# Endpoints "liste"
orders = make_list_handler("order", ORDERS, defaults={"status": "PENDING_PAYMENT"})
clients = make_list_handler("client", CLIENTS)
partners = make_list_handler("partner", PARTNERS)
payments = make_list_handler("payment", PAYMENTS)
incidents = make_list_handler("incident", INCIDENTS)

# ===== Changement de statut d'une commande =====
@csrf_exempt
def order_status(request, oid: int):
    if request.method == "OPTIONS":
        return add_cors(HttpResponse(status=204))
    if request.method != "POST":
        return add_cors(JsonResponse({"error": "POST only"}, status=405))

    order = find_order(oid)
    if not order:
        return add_cors(JsonResponse({"error": f"Order {oid} not found"}, status=404))

    payload = parse_json(request) or {}
    # 2 modes : action=next OU status="READY" (par ex)
    if payload.get("action") == "next":
        current = order["status"]
        if current not in NEXT_STATUS:
            return add_cors(JsonResponse({"error": f"No next status from {current}"}, status=400))
        order["status"] = NEXT_STATUS[current]
        order["status_changed_at"] = now().isoformat()
        return add_cors(JsonResponse({"ok": True, "data": order}, status=200))

    new_status = payload.get("status")
    if new_status:
        if new_status not in ORDER_STATUSES:
            return add_cors(JsonResponse({"error": f"Invalid status {new_status}"}, status=400))
        order["status"] = new_status
        order["status_changed_at"] = now().isoformat()
        return add_cors(JsonResponse({"ok": True, "data": order}, status=200))

    return add_cors(JsonResponse({"error": "Provide {'action':'next'} or {'status':'READY'}"}, status=400))

# ===== Routes =====
urlpatterns = [
    path("", home),
    path("api/health/", health),

    path("api/orders/", orders),
    path("api/orders/<int:oid>/status/", order_status),  # << nouveau

    path("api/clients/", clients),
    path("api/partners/", partners),
    path("api/payments/", payments),
    path("api/incidents/", incidents),

    path("favicon.ico", favicon),
]
