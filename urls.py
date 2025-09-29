from django.urls import path
from django.http import HttpResponse, JsonResponse
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
import json

ORDERS, CLIENTS, PARTNERS, PAYMENTS, INCIDENTS = [], [], [], [], []
NEXT_ID = {"order":1,"client":1,"partner":1,"payment":1,"incident":1}
ORDER_STATUSES = ["PENDING_PAYMENT","PAID","COLLECTING","PROCESSING","READY","DELIVERING","DELIVERED"]
NEXT_STATUS = {"PENDING_PAYMENT":"PAID","PAID":"COLLECTING","COLLECTING":"PROCESSING","PROCESSING":"READY","READY":"DELIVERING","DELIVERING":"DELIVERED"}

def add_cors(r):
    r["Access-Control-Allow-Origin"]="*"
    r["Access-Control-Allow-Headers"]="Content-Type, Authorization"
    r["Access-Control-Allow-Methods"]="GET, POST, OPTIONS"
    return r

def parse_json(request):
    try:
        return json.loads(request.body.decode("utf-8") or "{}")
    except Exception:
        return None

def home(_): return add_cors(HttpResponse("FAGNI API – OK", status=200))
def health(_): return add_cors(JsonResponse({"ok":True,"time":now().isoformat()}))
def favicon(_): return add_cors(HttpResponse(status=204))

def make_list_handler(store_key, store, defaults=None):
    @csrf_exempt
    def h(request):
        if request.method=="OPTIONS": return add_cors(HttpResponse(status=204))
        if request.method=="GET": return add_cors(JsonResponse({"ok":True,"data":store}, safe=False))
        if request.method=="POST":
            p = parse_json(request)
            if p is None: return add_cors(JsonResponse({"error":"Invalid JSON"}, status=400))
            p["id"] = NEXT_ID[store_key]; NEXT_ID[store_key]+=1
            p.setdefault("created_at", now().isoformat())
            if defaults:
                for k,v in defaults.items(): p.setdefault(k,v)
            if store_key=="order":
                p.setdefault("items", [])
                p.setdefault("status", "PENDING_PAYMENT")
                p["history"] = [{"status":p["status"], "at": now().isoformat()}]
            store.append(p)
            return add_cors(JsonResponse({"ok":True,"data":p}, status=201))
        return add_cors(JsonResponse({"error":"Method not allowed"}, status=405))
    return h

orders   = make_list_handler("order",   ORDERS,   defaults={"status":"PENDING_PAYMENT"})
clients  = make_list_handler("client",  CLIENTS)
partners = make_list_handler("partner", PARTNERS)
payments = make_list_handler("payment", PAYMENTS)
incidents= make_list_handler("incident",INCIDENTS)

@csrf_exempt
def order_status(request, oid:int):
    if request.method=="OPTIONS": return add_cors(HttpResponse(status=204))
    if request.method!="POST": return add_cors(JsonResponse({"error":"POST only"}, status=405))
    try:
        order = next(o for o in ORDERS if o["id"]==oid)
    except StopIteration:
        return add_cors(JsonResponse({"error":f"Order {oid} not found"}, status=404))
    p = parse_json(request) or {}
    if p.get("action")=="next":
        cur = order["status"]
        nxt = NEXT_STATUS.get(cur)
        if not nxt: return add_cors(JsonResponse({"error":f"No next from {cur}"}, status=400))
        order["status"] = nxt
    elif "status" in p:
        if p["status"] not in ORDER_STATUSES:
            return add_cors(JsonResponse({"error":"Invalid status"}, status=400))
        order["status"] = p["status"]
    else:
        return add_cors(JsonResponse({"error":"Provide {'action':'next'} or {'status':'READY'}"}, status=400))
    order.setdefault("history", []).append({"status":order["status"], "at":now().isoformat()})
    return add_cors(JsonResponse({"ok":True,"data":order}))
    
urlpatterns = [
    path("", home),
    path("api/health/", health),
    path("api/orders/", orders),
    path("api/orders/<int:oid>/status/", order_status),
    path("api/clients/", clients),
    path("api/partners/", partners),
    path("api/payments/", payments),
    path("api/incidents/", incidents),
    path("favicon.ico", favicon),
]
