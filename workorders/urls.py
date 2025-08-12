from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WorkOrderViewSet, WorkOrderItemViewSet

router = DefaultRouter()
router.register(r"ot", WorkOrderViewSet, basename="workorder")
router.register(r"ot-items", WorkOrderItemViewSet, basename="workorderitem")

urlpatterns = [
    path("", include(router.urls)),
]