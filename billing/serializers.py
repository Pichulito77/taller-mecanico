from django.db import transaction
from rest_framework import serializers

from .models import Invoice, InvoiceItem, Quote, QuoteItem


class QuoteItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuoteItem
        fields = [
            "id",
            "presupuesto",
            "tipo",
            "repuesto_id",
            "descripcion",
            "cantidad",
            "precio_unitario",
            "impuestos",
            "total",
        ]
        read_only_fields = ("total",)


class QuoteSerializer(serializers.ModelSerializer):
    items = QuoteItemSerializer(many=True, read_only=True)

    class Meta:
        model = Quote
        fields = [
            "id",
            "numero",
            "cliente",
            "vehiculo",
            "creado_por_user_id",
            "estado",
            "observaciones",
            "fecha_emision",
            "subtotal",
            "impuestos",
            "descuento",
            "total",
            "items",
        ]
        read_only_fields = ("subtotal", "impuestos", "total")

    def create(self, validated_data):
        # Evitar FK hacia app_user; dejamos NULL
        validated_data["creado_por_user_id"] = None
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # No permitir setear creado_por_user_id; mantener o poner NULL
        if "creado_por_user_id" in validated_data:
            validated_data["creado_por_user_id"] = instance.creado_por_user_id or None
        return super().update(instance, validated_data)


class InvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItem
        fields = [
            "id",
            "factura",
            "tipo",
            "repuesto_id",
            "descripcion",
            "cantidad",
            "precio_unitario",
            "impuestos",
            "total",
        ]
        read_only_fields = ("total",)


class InvoiceSerializer(serializers.ModelSerializer):
    items = InvoiceItemSerializer(many=True, read_only=True)

    class Meta:
        model = Invoice
        fields = [
            "id",
            "numero",
            "cliente",
            "vehiculo",
            "presupuesto",
            "ot_id",
            "emitida_por_user_id",
            "estado",
            "fecha_emision",
            "moneda",
            "subtotal",
            "impuestos",
            "descuento",
            "total",
            "items",
        ]
        read_only_fields = ("subtotal", "impuestos", "total")


@transaction.atomic
def emit_invoice_from_quote(
    quote: Quote, numero_factura: str, emitida_por_user_id: int | None
) -> Invoice:
    # Crear factura copiando header
    inv = Invoice.objects.create(
        numero=numero_factura,
        cliente=quote.cliente,
        vehiculo=quote.vehiculo,
        presupuesto=quote,
        ot_id=None,
        emitida_por_user_id=None,  # avoid FK to app_user
        estado="emitida",
        fecha_emision=quote.fecha_emision,
        moneda="ARS",
        subtotal=quote.subtotal,
        impuestos=quote.impuestos,
        descuento=quote.descuento,
        total=quote.total,
    )
    # Copiar items
    for qi in quote.items.all():
        InvoiceItem.objects.create(
            factura=inv,
            tipo=qi.tipo,
            repuesto_id=qi.repuesto_id,
            descripcion=qi.descripcion,
            cantidad=qi.cantidad,
            precio_unitario=qi.precio_unitario,
            impuestos=qi.impuestos,
            total=qi.total,
        )
    # Cambiar estado del presupuesto
    quote.estado = "aprobado"
    quote.save(update_fields=["estado"])
    return inv
