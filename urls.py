from django.urls import path
from django.http import HttpResponse, JsonResponse
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
import json

# ===== Données en mémoire (reset à chaque redeploy) =====
ORDERS, CLIENTS, PARTNERS, PAYMENTS, INCIDENTS = [], [], [], [], []
NEXT_ID = {"order": 1, "client": 1, "partner": 1, "payment": 1, "incident": 1}

# ===== Workflow =====
ORDER_STATUSES = ["PENDING_PAYMENT","PAID","COLLECTING","PROCESSING","READY","DELIVERING","DELIVERED"]
NEXT_STATUS = {
    "PENDING_PAYMENT":"PAID","PAID":"COLLECTING","COLLECTING":"PROCESSING",
    "PROCESSING":"READY","READY":"DELIVERING","DELIVERING":"DELIVERED"
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

def compute_total(items):
    try:
        return sum(int(i.get("qty",1))*int(i.get("price",0)) for i in (items or []))
    except Exception:
        return 0

def find(store, _id):
    for o in store:
        if o.get("id") == _id:
            return o
    return None

# ===== Pages simples =====
def home(_): return add_cors(HttpResponse("FAGNI API – OK", status=200))
def health(_): return add_cors(JsonResponse({"ok":True,"time":now().isoformat()}))
def favicon(_): return add_cors(HttpResponse(status=204))

# ===== Fabrique (GET liste / POST création) =====
def make_list_handler(store_key, store, defaults=None):
    @csrf_exempt
    def handler(request):
        if request.method == "OPTIONS": return add_cors(HttpResponse(status=204))

        if request.method == "GET":
            return add_cors(JsonResponse({"ok": True, "data": store}, safe=False))

        if request.method == "POST":
            payload = parse_json(request)
            if payload is None:
                return add_cors(JsonResponse({"error":"Invalid JSON"}, status=400))
            payload["id"] = NEXT_ID[store_key]; NEXT_ID[store_key] += 1
            payload.setdefault("created_at", now().isoformat())
            if defaults:
                for k,v in defaults.items(): payload.setdefault(k,v)

            if store_key == "order":
                payload.setdefault("items", [])
                payload.setdefault("status", "PENDING_PAYMENT")
                # nouveaux champs facultatifs
                payload.setdefault("partner_id", None)
                payload.setdefault("pickup_at", None)
                payload.setdefault("delivery_at", None)
                # total automatique si non fourni
                if "total" not in payload:
                    payload["total"] = compute_total(payload.get("items", []))
                # historique
                payload["history"] = payload.get("history", [])
                payload["history"].append({"status": payload["status"], "at": now().isoformat()})

            store.append(payload)
            return add_cors(JsonResponse({"ok": True, "data": payload}, status=201))

        return add_cors(JsonResponse({"error":"Method not allowed"}, status=405))
    return handler

orders = make_list_handler("order", ORDERS, defaults={"status":"PENDING_PAYMENT"})
clients = make_list_handler("client", CLIENTS)
partners = make_list_handler("partner", PARTNERS)
payments = make_list_handler("payment", PAYMENTS)
incidents = make_list_handler("incident", INCIDENTS)

# ===== Changer le statut d'une commande =====
@csrf_exempt
def order_status(request, oid:int):
    if request.method == "OPTIONS": return add_cors(HttpResponse(status=204))
    if request.method != "POST": return add_cors(JsonResponse({"error":"POST only"}, status=405))
    order = find(ORDERS, oid)
    if not order: return add_cors(JsonResponse({"error":f"Order {oid} not found"}, status=404))

    payload = parse_json(request) or {}
    if payload.get("action") == "next":
        cur = order["status"]
        if cur not in NEXT_STATUS:
            return add_cors(JsonResponse({"error":f"No next status from {cur}"}, status=400))
        order["status"] = NEXT_STATUS[cur]
    elif "status" in payload:
        new = payload["status"]
        if new not in ORDER_STATUSES:
            return add_cors(JsonResponse({"error":f"Invalid status {new}"}, status=400))
        order["status"] = new
    else:
        return add_cors(JsonResponse({"error":"Provide {'action':'next'} or {'status':'READY'}"}, status=400))

    order.setdefault("history", []).append({"status": order["status"], "at": now().isoformat()})
    order["status_changed_at"] = now().isoformat()
    return add_cors(JsonResponse({"ok":True,"data":order}, status=200))

# ===== Assigner un partenaire =====
@csrf_exempt
def order_assign(request, oid:int):
    if request.method == "OPTIONS": return add_cors(HttpResponse(status=204))
    if request.method != "POST": return add_cors(JsonResponse({"error":"POST only"}, status=405))
    order = find(ORDERS, oid)
    if not order: return add_cors(JsonResponse({"error":f"Order {oid} not found"}, status=404))
    p = parse_json(request) or {}
    order["partner_id"] = p.get("partner_id")
    return add_cors(JsonResponse({"ok":True, "data": order}, status=200))

# ===== Planifier collecte / livraison =====
@csrf_exempt
def order_schedule(request, oid:int):
    if request.method == "OPTIONS": return add_cors(HttpResponse(status=204))
    if request.method != "POST": return add_cors(JsonResponse({"error":"POST only"}, status=405))
    order = find(ORDERS, oid)
    if not order: return add_cors(JsonResponse({"error":f"Order {oid} not found"}, status=404))
    p = parse_json(request) or {}
    order["pickup_at"] = p.get("pickup_at")
    order["delivery_at"] = p.get("delivery_at")
    return add_cors(JsonResponse({"ok":True, "data": order}, status=200))

# ===== Routes =====
urlpatterns = [
    path("", home),
    path("api/health/", health),

    path("api/orders/", orders),
    path("api/orders/<int:oid>/status/", order_status),
    path("api/orders/<int:oid>/assign/", order_assign),
    path("api/orders/<int:oid>/schedule/", order_schedule),

    path("api/clients/", clients),
    path("api/partners/", partners),
    path("api/payments/", payments),
    path("api/incidents/", incidents),

    path("favicon.ico", favicon),
        ]
