from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PartViewSet, InventoryMoveViewSet

router = DefaultRouter()
router.register(r"repuestos", PartViewSet, basename="repuesto")
router.register(r"movimientos", InventoryMoveViewSet, basename="movimiento")

urlpatterns = [
    path("", include(router.urls)),
]