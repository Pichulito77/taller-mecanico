from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ClienteViewSet, VehiculoViewSet

router = DefaultRouter()
router.register(r"clientes", ClienteViewSet, basename="cliente")
router.register(r"vehiculos", VehiculoViewSet, basename="vehiculo")

urlpatterns = [
    path("", include(router.urls)),
]
