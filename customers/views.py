from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import QuerySet
from .models import Cliente, Vehiculo
from .serializers import ClienteSerializer, VehiculoSerializer


class IsAuthenticatedModelPermissions(permissions.DjangoModelPermissions):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return super().has_permission(request, view)


class ClienteViewSet(viewsets.ModelViewSet):
    queryset: QuerySet[Cliente] = Cliente.objects.all().order_by("razon_social", "id")
    serializer_class = ClienteSerializer
    permission_classes = [IsAuthenticatedModelPermissions]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["razon_social", "documento", "email"]
    filterset_fields = ["documento", "ciudad", "provincia"]


class VehiculoViewSet(viewsets.ModelViewSet):
    queryset: QuerySet[Vehiculo] = (
        Vehiculo.objects.select_related("cliente").all().order_by("placa")
    )
    serializer_class = VehiculoSerializer
    permission_classes = [IsAuthenticatedModelPermissions]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["placa", "vin", "marca", "modelo", "cliente__razon_social"]
    filterset_fields = {"cliente": ["exact"], "placa": ["exact"], "vin": ["exact"]}