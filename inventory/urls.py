from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import InventoryMoveViewSet, PartViewSet

router = DefaultRouter()
router.register(r"repuestos", PartViewSet, basename="repuesto")
router.register(r"movimientos", InventoryMoveViewSet, basename="movimiento")

urlpatterns = [
    path("", include(router.urls)),
]
