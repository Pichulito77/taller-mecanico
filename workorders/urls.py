from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import WorkOrderItemViewSet, WorkOrderViewSet

router = DefaultRouter()
router.register(r"ot", WorkOrderViewSet, basename="workorder")
router.register(r"ot-items", WorkOrderItemViewSet, basename="workorderitem")

urlpatterns = [
    path("", include(router.urls)),
]
