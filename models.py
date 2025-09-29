
from django.db import models

class Client(models.Model):
    full_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=40, db_index=True)
    email = models.EmailField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    preferred_slot = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return f"{self.full_name} ({self.phone})"

class Partner(models.Model):
    TYPE_CHOICES = [("blanchisserie","Blanchisserie"),("couture","Couture"),("cordonnerie","Cordonnerie")]
    name = models.CharField(max_length=150)
    type = models.CharField(max_length=40, choices=TYPE_CHOICES)
    contact = models.CharField(max_length=60, blank=True, null=True)
    zones = models.JSONField(default=list, blank=True)
    commission_rate = models.DecimalField(max_digits=4, decimal_places=2, default=0.18)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.name

class Order(models.Model):
    STATUS = [
        ("PENDING_PAYMENT","PENDING_PAYMENT"),
        ("PAID","PAID"),
        ("COLLECTING","COLLECTING"),
        ("PROCESSING","PROCESSING"),
        ("READY","READY"),
        ("DELIVERING","DELIVERING"),
        ("DELIVERED","DELIVERED"),
    ]
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=40)
    client = models.ForeignKey(Client, null=True, blank=True, on_delete=models.SET_NULL)
    items = models.JSONField(default=list, blank=True)  # [{label, qty, price}]
    total = models.IntegerField(default=0)
    note = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=30, choices=STATUS, default="PENDING_PAYMENT", db_index=True)
    partner = models.ForeignKey(Partner, null=True, blank=True, on_delete=models.SET_NULL)
    pickup_at = models.DateTimeField(null=True, blank=True)
    delivery_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return f"Order #{self.pk} - {self.name}"

class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="payments")
    method = models.CharField(max_length=30)   # momo, card, cash...
    amount = models.IntegerField()
    currency = models.CharField(max_length=10, default="XOF")
    status = models.CharField(max_length=30, default="paid")
    reference = models.CharField(max_length=80, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return f"Payment #{self.pk} - {self.amount} {self.currency}"

class Incident(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="incidents")
    type = models.CharField(max_length=60)
    severity = models.CharField(max_length=30, default="medium")
    description = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return f"Incident #{self.pk} - {self.type}"
