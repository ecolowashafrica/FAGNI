from django.http import HttpResponse
from django.urls import path

def favicon(_):
    # Réponse vide (no content) pour éviter un 404
    return HttpResponse(status=204)

urlpatterns = [
    path("", home),                # si tu as déjà une page d'accueil
    path("api/health/", health),
    path("favicon.ico", favicon),  # ← évite le 404
]
