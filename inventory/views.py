from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import QuerySet
from .models import Part, InventoryMove
from .serializers import PartSerializer, InventoryMoveSerializer


class IsAuthenticatedModelPermissions(permissions.DjangoModelPermissions):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return super().has_permission(request, view)


class PartViewSet(viewsets.ModelViewSet):
    queryset: QuerySet[Part] = Part.objects.all().order_by("sku")
    serializer_class = PartSerializer
    permission_classes = [IsAuthenticatedModelPermissions]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["sku", "nombre"]
    filterset_fields = {"stock_minimo": ["lte"], "stock_actual": ["lte", "gte"]}


class InventoryMoveViewSet(viewsets.ModelViewSet):
    queryset: QuerySet[InventoryMove] = InventoryMove.objects.select_related("repuesto").all()
    serializer_class = InventoryMoveSerializer
    permission_classes = [IsAuthenticatedModelPermissions]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["tipo", "repuesto__sku", "repuesto__nombre", "referencia"]
    filterset_fields = {"repuesto": ["exact"], "tipo": ["exact"]}