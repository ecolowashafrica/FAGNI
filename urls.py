
from django.urls import path
from . import views

urlpatterns = [
    path("clients/", views.clients),
    path("orders/", views.orders),
    path("orders/<int:pk>/status/", views.order_status),
    path("orders/<int:pk>/assign/", views.order_assign),
    path("orders/<int:pk>/schedule/", views.order_schedule),
    path("partners/", views.partners),
    path("payments/", views.payments),
    path("incidents/", views.incidents),
]
