
from rest_framework import serializers
from .models import Client, Partner, Order, Payment, Incident

class ClientSerializer(serializers.ModelSerializer):
    class Meta: model = Client; fields = "__all__"

class PartnerSerializer(serializers.ModelSerializer):
    class Meta: model = Partner; fields = "__all__"

class OrderSerializer(serializers.ModelSerializer):
    class Meta: model = Order; fields = "__all__"

class PaymentSerializer(serializers.ModelSerializer):
    class Meta: model = Payment; fields = "__all__"

class IncidentSerializer(serializers.ModelSerializer):
    class Meta: model = Incident; fields = "__all__"
