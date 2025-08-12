from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import QuerySet
from .models import Quote, QuoteItem, Invoice, InvoiceItem
from .serializers import QuoteSerializer, QuoteItemSerializer, InvoiceSerializer, InvoiceItemSerializer, emit_invoice_from_quote


class IsAuthenticatedModelPermissions(permissions.DjangoModelPermissions):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return super().has_permission(request, view)


class QuoteViewSet(viewsets.ModelViewSet):
    queryset: QuerySet[Quote] = Quote.objects.all().order_by("-id")
    serializer_class = QuoteSerializer
    permission_classes = [IsAuthenticatedModelPermissions]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["numero", "cliente__razon_social", "vehiculo__placa"]
    filterset_fields = {"cliente": ["exact"], "vehiculo": ["exact"], "estado": ["exact"]}

    @action(detail=True, methods=["post"], url_path="emitir")
    def emitir(self, request, pk=None):
        quote = self.get_object()
        numero_factura = request.data.get("numero")
        if not numero_factura:
            return Response({"numero": ["Requerido"]}, status=status.HTTP_400_BAD_REQUEST)
        inv = emit_invoice_from_quote(quote, numero_factura, getattr(request.user, "id", None))
        return Response(InvoiceSerializer(inv).data, status=status.HTTP_201_CREATED)


class QuoteItemViewSet(viewsets.ModelViewSet):
    queryset: QuerySet[QuoteItem] = QuoteItem.objects.select_related("presupuesto").all()
    serializer_class = QuoteItemSerializer
    permission_classes = [IsAuthenticatedModelPermissions]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["descripcion", "tipo"]
    filterset_fields = {"presupuesto": ["exact"], "tipo": ["exact"]}


class InvoiceViewSet(viewsets.ModelViewSet):
    queryset: QuerySet[Invoice] = Invoice.objects.all().order_by("-id")
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticatedModelPermissions]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["numero", "cliente__razon_social", "vehiculo__placa"]
    filterset_fields = {"cliente": ["exact"], "vehiculo": ["exact"], "estado": ["exact"]}


class InvoiceItemViewSet(viewsets.ModelViewSet):
    queryset: QuerySet[InvoiceItem] = InvoiceItem.objects.select_related("factura").all()
    serializer_class = InvoiceItemSerializer
    permission_classes = [IsAuthenticatedModelPermissions]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["descripcion", "tipo"]
    filterset_fields = {"factura": ["exact"], "tipo": ["exact"]}