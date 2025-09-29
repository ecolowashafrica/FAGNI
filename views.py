from rest_framework import viewsets, permissions
from .models import Order
from .serializers import OrderSerializer
class OrdersViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('-created_at')
    serializer_class = OrderSerializer
    permission_classes = [permissions.AllowAny]
