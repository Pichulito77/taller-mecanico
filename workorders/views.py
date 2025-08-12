from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import QuerySet
from .models import WorkOrder, WorkOrderItem
from .serializers import WorkOrderSerializer, WorkOrderItemSerializer


class IsAuthenticatedModelPermissions(permissions.DjangoModelPermissions):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return super().has_permission(request, view)


class WorkOrderViewSet(viewsets.ModelViewSet):
    queryset: QuerySet[WorkOrder] = (
        WorkOrder.objects.select_related("cliente", "vehiculo").all().order_by("-id")
    )
    serializer_class = WorkOrderSerializer
    permission_classes = [IsAuthenticatedModelPermissions]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["numero", "cliente__razon_social", "vehiculo__placa", "estado"]
    filterset_fields = {
        "estado": ["exact"],
        "cliente": ["exact"],
        "vehiculo": ["exact"],
        "asignado_a_user_id": ["exact"],
    }


class WorkOrderItemViewSet(viewsets.ModelViewSet):
    queryset: QuerySet[WorkOrderItem] = WorkOrderItem.objects.select_related("workorder").all()
    serializer_class = WorkOrderItemSerializer
    permission_classes = [IsAuthenticatedModelPermissions]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["descripcion", "tipo"]
    filterset_fields = {"workorder": ["exact"], "tipo": ["exact"]}