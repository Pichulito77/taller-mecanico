from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models import DecimalField, F
import os

from customers.models import Cliente, Vehiculo

MANAGED = os.getenv("USE_SQLITE", "false").lower() == "true"


class WorkOrder(models.Model):
    id = models.BigAutoField(db_column="ot_id", primary_key=True)
    numero = models.CharField(max_length=30, unique=True)
    cliente = models.ForeignKey(
        Cliente, on_delete=models.RESTRICT, db_column="cliente_id", related_name="ordenes"
    )
    vehiculo = models.ForeignKey(
        Vehiculo, on_delete=models.RESTRICT, db_column="vehiculo_id", related_name="ordenes"
    )
    asignado_a_user_id = models.BigIntegerField(
        db_column="asignado_a_user_id", null=True, blank=True, default=None
    )

    # Nuevos campos
    fecha_ingreso = models.DateTimeField(null=True, blank=True, db_column="fecha_ingreso")
    fecha_salida = models.DateTimeField(null=True, blank=True, db_column="fecha_salida")
    matricula = models.CharField(max_length=20, null=True, blank=True, db_column="matricula")
    color = models.CharField(max_length=30, null=True, blank=True, db_column="color")
    kilometraje = models.IntegerField(null=True, blank=True, db_column="kilometraje")
    ingresado_en_grua = models.BooleanField(default=False, db_column="ingresado_en_grua")
    datos_adicionales = models.TextField(null=True, blank=True, db_column="datos_adicionales")

    ESTADOS = (
        ("abierta", "Abierta"),
        ("en_progreso", "En progreso"),
        ("finalizada", "Finalizada"),
        ("anulada", "Anulada"),
    )
    estado = models.CharField(max_length=12, choices=ESTADOS, default="abierta")

    # Totales
    subtotal = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    impuestos = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    descuento = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    fecha_apertura = models.DateTimeField(auto_now_add=True)
    fecha_cierre = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "orden_trabajo"
        managed = MANAGED
        verbose_name = "Orden de Trabajo"
        verbose_name_plural = "Órdenes de Trabajo"


class WorkOrderItem(models.Model):
    id = models.BigAutoField(db_column="ot_item_id", primary_key=True)
    workorder = models.ForeignKey(
        WorkOrder, on_delete=models.CASCADE, db_column="ot_id", related_name="items"
    )
    TIPO = (("repuesto", "Repuesto"), ("mano_obra", "Mano de obra"))
    tipo = models.CharField(max_length=12, choices=TIPO)
    repuesto_id = models.BigIntegerField(null=True, blank=True)
    descripcion = models.TextField()
    cantidad = models.DecimalField(max_digits=12, decimal_places=3)
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2)
    impuestos = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    if hasattr(models, "GeneratedField"):
        total = models.GeneratedField(
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
        db_table = "ot_item"
        managed = MANAGED
        verbose_name = "Ítem de OT"
        verbose_name_plural = "Ítems de OT"
