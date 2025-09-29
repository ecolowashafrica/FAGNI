from django.urls import path
from django.http import HttpResponse
from django.utils.timezone import now

def home(request):
    return HttpResponse("FAGNI API – OK", status=200)

def health(request):
    return HttpResponse(
        f'{{"ok": true, "time": "{now().isoformat()}"}}',
        content_type="application/json",
        status=200,
    )

urlpatterns = [
    path("", home),              # ← / renvoie 200 au lieu de 404
    path("api/health/", health),
]
