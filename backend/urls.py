from django.contrib import admin
from django.http import JsonResponse
from django.urls import path, include


def health_view(_request):
    return JsonResponse({"status": "ok"})


urlpatterns = [
    path("admin/", admin.site.urls),
    path("health/", health_view, name="health"),
    path("api/", include("customers.urls")),
    path("api/", include("workorders.urls")),
    path("api/", include("inventory.urls")),
]