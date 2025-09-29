
from django.contrib import admin
from .models import Client, Partner, Order, Payment, Incident

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("id","full_name","phone","email","created_at")
    search_fields = ("full_name","phone","email")

@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ("id","name","type","contact","commission_rate","created_at")
    search_fields = ("name","contact")
    list_filter = ("type",)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id","name","phone","total","status","partner","pickup_at","delivery_at","created_at")
    search_fields = ("name","phone")
    list_filter = ("status","partner")

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("id","order","method","amount","currency","status","reference","created_at")
    list_filter = ("method","status")

@admin.register(Incident)
class IncidentAdmin(admin.ModelAdmin):
    list_display = ("id","order","type","severity","created_at")
    list_filter = ("severity",)
