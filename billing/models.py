from django.db import models
from django.db.models import DecimalField, F
import os

from customers.models import Cliente, Vehiculo

MANAGED = os.getenv("USE_SQLITE", "false").lower() == "true"

try:
    from django.db.models import GeneratedField  # Django 5+
except Exception:  # pragma: no cover
    GeneratedField = None


class Quote(models.Model):  # presupuesto
    id = models.BigAutoField(db_column="presupuesto_id", primary_key=True)
    numero = models.CharField(max_length=30, unique=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.RESTRICT, db_column="cliente_id")
    vehiculo = models.ForeignKey(
        Vehiculo, on_delete=models.SET_NULL, null=True, db_column="vehiculo_id"
    )
    creado_por_user_id = models.BigIntegerField(db_column="creado_por_user_id", null=True)
    ESTADOS = (
        ("borrador", "Borrador"),
        ("aprobado", "Aprobado"),
        ("rechazado", "Rechazado"),
        ("anulado", "Anulado"),
    )
    estado = models.CharField(max_length=12, choices=ESTADOS, default="borrador")
    observaciones = models.TextField(null=True, blank=True)
    fecha_emision = models.DateTimeField()
    subtotal = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    impuestos = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    descuento = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    class Meta:
        db_table = "presupuesto"
        managed = MANAGED
        ordering = ["-id"]

    def clean(self) -> None:
        if not self.creado_por_user_id or self.creado_por_user_id == 0:
            self.creado_por_user_id = None


class QuoteItem(models.Model):  # presupuesto_item
    id = models.BigAutoField(db_column="presupuesto_item_id", primary_key=True)
    presupuesto = models.ForeignKey(
        Quote, on_delete=models.CASCADE, db_column="presupuesto_id", related_name="items"
    )
    TIPO = (("repuesto", "Repuesto"), ("mano_obra", "Mano de obra"))
    tipo = models.CharField(max_length=12, choices=TIPO)
    repuesto_id = models.BigIntegerField(null=True, blank=True)
    descripcion = models.TextField()
    cantidad = models.DecimalField(max_digits=12, decimal_places=3)
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2)
    impuestos = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    if GeneratedField:
        total = GeneratedField(
            expression=F("cantidad") * F("precio_unitario") + F("impuestos"),
            output_field=DecimalField(max_digits=14, decimal_places=2),
            db_persist=True,
            db_column="total",
        )
    else:
        total = models.DecimalField(
            max_digits=14, decimal_places=2, editable=False, db_column="total"
        )

    class Meta:
        db_table = "presupuesto_item"
        managed = MANAGED
        ordering = ["id"]


class Invoice(models.Model):  # factura
    id = models.BigAutoField(db_column="factura_id", primary_key=True)
    numero = models.CharField(max_length=30, unique=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.RESTRICT, db_column="cliente_id")
    vehiculo = models.ForeignKey(
        Vehiculo, on_delete=models.SET_NULL, null=True, db_column="vehiculo_id"
    )
    presupuesto = models.ForeignKey(
        Quote, on_delete=models.SET_NULL, null=True, db_column="presupuesto_id"
    )
    ot_id = models.BigIntegerField(db_column="ot_id", null=True)
    emitida_por_user_id = models.BigIntegerField(db_column="emitida_por_user_id", null=True)
    estado = models.CharField(max_length=10)
    fecha_emision = models.DateTimeField()
    moneda = models.CharField(max_length=3)
    subtotal = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    impuestos = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    descuento = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    class Meta:
        db_table = "factura"
        managed = MANAGED
        ordering = ["-id"]


class InvoiceItem(models.Model):  # factura_item
    id = models.BigAutoField(db_column="factura_item_id", primary_key=True)
    factura = models.ForeignKey(
        Invoice, on_delete=models.CASCADE, db_column="factura_id", related_name="items"
    )
    TIPO = (("repuesto", "Repuesto"), ("mano_obra", "Mano de obra"))
    tipo = models.CharField(max_length=12, choices=TIPO)
    repuesto_id = models.BigIntegerField(null=True, blank=True)
    descripcion = models.TextField()
    cantidad = models.DecimalField(max_digits=12, decimal_places=3)
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2)
    impuestos = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    if GeneratedField:
        total = GeneratedField(
            expression=F("cantidad") * F("precio_unitario") + F("impuestos"),
            output_field=DecimalField(max_digits=14, decimal_places=2),
            db_persist=True,
            db_column="total",
        )
    else:
        total = models.DecimalField(
            max_digits=14, decimal_places=2, editable=False, db_column="total"
        )

    class Meta:
        db_table = "factura_item"
        managed = MANAGED
        ordering = ["id"]
