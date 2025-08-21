from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import InvoiceItemViewSet, InvoiceViewSet, QuoteItemViewSet, QuoteViewSet

router = DefaultRouter()
router.register(r"presupuestos", QuoteViewSet, basename="presupuesto")
router.register(r"presupuesto-items", QuoteItemViewSet, basename="presupuestoitem")
router.register(r"facturas", InvoiceViewSet, basename="factura")
router.register(r"factura-items", InvoiceItemViewSet, basename="facturaitem")

urlpatterns = [
    path("", include(router.urls)),
]
