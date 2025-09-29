from django.db import models
class Order(models.Model):
    STATUS = [
        ('PENDING_PAYMENT','Pending Payment'),
        ('PAID','Paid'),
        ('COLLECTING','Collecting'),
        ('PROCESSING','Processing'),
        ('READY','Ready'),
        ('DELIVERING','Delivering'),
        ('DELIVERED','Delivered'),
        ('CANCELED','Canceled'),
    ]
    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=30)
    items = models.JSONField(default=list)
    total = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS, default='PENDING_PAYMENT')
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return f"Order #{self.id} - {self.name}"
