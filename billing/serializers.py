from decimal import Decimal
from django.db import transaction
from rest_framework import serializers
from .models import Quote, QuoteItem, Invoice, InvoiceItem


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
def emit_invoice_from_quote(quote: Quote, numero_factura: str, emitida_por_user_id: int | None) -> Invoice:
    # Crear factura copiando header
    inv = Invoice.objects.create(
        numero=numero_factura,
        cliente=quote.cliente,
        vehiculo=quote.vehiculo,
        presupuesto=quote,
        ot_id=None,
        emitida_por_user_id=emitida_por_user_id,
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