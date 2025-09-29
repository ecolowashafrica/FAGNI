from django.urls import path
from django.http import JsonResponse
import json

# stockage en mémoire
ORDERS, CLIENTS, PARTNERS, PAYMENTS, INCIDENTS = [], [], [], [], []

def home(request):
    return JsonResponse({"message": "FAGNI backend actif"})

# ---- CLIENTS ----
def clients(request):
    if request.method == "POST":
        data = json.loads(request.body)
        data["id"] = len(CLIENTS) + 1
        CLIENTS.append(data)
        return JsonResponse({"success": True, "client": data})
    return JsonResponse({"data": CLIENTS})

# ---- ORDERS ----
def orders(request):
    if request.method == "POST":
        data = json.loads(request.body)
        data["id"] = len(ORDERS) + 1
        ORDERS.append(data)
        return JsonResponse({"success": True, "order": data})
    return JsonResponse({"data": ORDERS})

# ---- PARTNERS ----
def partners(request):
    if request.method == "POST":
        data = json.loads(request.body)
        data["id"] = len(PARTNERS) + 1
        PARTNERS.append(data)
        return JsonResponse({"success": True, "partner": data})
    return JsonResponse({"data": PARTNERS})

# ---- PAYMENTS ----
def payments(request):
    if request.method == "POST":
        data = json.loads(request.body)
        data["id"] = len(PAYMENTS) + 1
        PAYMENTS.append(data)
        return JsonResponse({"success": True, "payment": data})
    return JsonResponse({"data": PAYMENTS})

# ---- INCIDENTS ----
def incidents(request):
    if request.method == "POST":
        data = json.loads(request.body)
        data["id"] = len(INCIDENTS) + 1
        INCIDENTS.append(data)
        return JsonResponse({"success": True, "incident": data})
    return JsonResponse({"data": INCIDENTS})

urlpatterns = [
    path("", home),
    path("api/clients/", clients),
    path("api/orders/", orders),
    path("api/partners/", partners),
    path("api/payments/", payments),
    path("api/incidents/", incidents),
]
