
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q
from .models import Client, Partner, Order, Payment, Incident
from .serializers import ClientSerializer, PartnerSerializer, OrderSerializer, PaymentSerializer, IncidentSerializer

# ---- Clients ----
@api_view(["GET","POST"])
def clients(request):
    if request.method == "POST":
        s = ClientSerializer(data=request.data)
        if s.is_valid():
            s.save()
            return Response({"ok": True, "data": s.data})
        return Response({"ok": False, "errors": s.errors}, status=400)
    qs = Client.objects.all().order_by("-id")
    return Response({"data": ClientSerializer(qs, many=True).data})

# ---- Partners ----
@api_view(["GET","POST"])
def partners(request):
    if request.method == "POST":
        s = PartnerSerializer(data=request.data)
        if s.is_valid():
            s.save()
            return Response({"ok": True, "data": s.data})
        return Response({"ok": False, "errors": s.errors}, status=400)
    qs = Partner.objects.all().order_by("-id")
    return Response({"data": PartnerSerializer(qs, many=True).data})

# ---- Orders ----
def _auto_total(items):
    try:
        return sum(int(x.get("qty",0))*int(x.get("price",0)) for x in items)
    except Exception:
        return 0

@api_view(["GET","POST"])
def orders(request):
    if request.method == "POST":
        data = request.data.copy()
        if not data.get("total"):
            data["total"] = _auto_total(data.get("items", []))
        s = OrderSerializer(data=data)
        if s.is_valid():
            s.save()
            return Response({"ok": True, "data": s.data})
        return Response({"ok": False, "errors": s.errors}, status=400)
    qs = Order.objects.all().order_by("-id")
    status_q = request.GET.get("status")
    q = request.GET.get("q")
    if status_q:
        qs = qs.filter(status=status_q)
    if q:
        qs = qs.filter(Q(name__icontains=q) | Q(phone__icontains=q))
    return Response({"data": OrderSerializer(qs, many=True).data})

@api_view(["POST"])
def order_status(request, pk):
    try:
        o = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response({"error":"Order not found"}, status=404)
    act = request.data.get("action")
    force = request.data.get("status")
    order = ["PENDING_PAYMENT","PAID","COLLECTING","PROCESSING","READY","DELIVERING","DELIVERED"]
    if act == "next":
        try:
            i = order.index(o.status)
            o.status = order[min(i+1, len(order)-1)]
        except ValueError:
            o.status = "PENDING_PAYMENT"
    elif force in order:
        o.status = force
    o.save()
    return Response({"ok": True, "data": OrderSerializer(o).data})

@api_view(["POST"])
def order_assign(request, pk):
    try:
        o = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response({"error":"Order not found"}, status=404)
    pid = request.data.get("partner_id")
    if not pid:
        return Response({"error":"partner_id required"}, status=400)
    try:
        p = Partner.objects.get(pk=pid)
    except Partner.DoesNotExist:
        return Response({"error":"Partner not found"}, status=404)
    o.partner = p
    o.save()
    return Response({"ok": True, "data": OrderSerializer(o).data})

@api_view(["POST"])
def order_schedule(request, pk):
    try:
        o = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response({"error":"Order not found"}, status=404)
    o.pickup_at = request.data.get("pickup_at") or o.pickup_at
    o.delivery_at = request.data.get("delivery_at") or o.delivery_at
    o.save()
    return Response({"ok": True, "data": OrderSerializer(o).data})

# ---- Payments ----
@api_view(["GET","POST"])
def payments(request):
    if request.method == "POST":
        s = PaymentSerializer(data=request.data)
        if s.is_valid():
            s.save()
            return Response({"ok": True, "data": s.data})
        return Response({"ok": False, "errors": s.errors}, status=400)
    qs = Payment.objects.all().order_by("-id")
    return Response({"data": PaymentSerializer(qs, many=True).data})

# ---- Incidents ----
@api_view(["GET","POST"])
def incidents(request):
    if request.method == "POST":
        s = IncidentSerializer(data=request.data)
        if s.is_valid():
            s.save()
            return Response({"ok": True, "data": s.data})
        return Response({"ok": False, "errors": s.errors}, status=400)
    qs = Incident.objects.all().order_by("-id")
    return Response({"data": IncidentSerializer(qs, many=True).data})
