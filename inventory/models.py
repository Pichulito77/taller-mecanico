from django.db import models
from django.db.models import DecimalField, F
import os

MANAGED = os.getenv("USE_SQLITE", "false").lower() == "true"


class Part(models.Model):
    id = models.BigAutoField(db_column="repuesto_id", primary_key=True)
    sku = models.CharField(max_length=60, unique=True)
    nombre = models.CharField(max_length=150)
    costo_unitario = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        db_table = "repuesto"
        managed = MANAGED
        verbose_name = "Repuesto"
        verbose_name_plural = "Repuestos"


class InventoryMove(models.Model):
    id = models.BigAutoField(db_column="movimiento_id", primary_key=True)
    repuesto = models.ForeignKey(Part, on_delete=models.RESTRICT, db_column="repuesto_id")
    tipo = models.CharField(max_length=10)  # entrada, salida, ajuste
    cantidad = models.DecimalField(max_digits=12, decimal_places=3)
    costo_unitario = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    if hasattr(models, "GeneratedField"):
        total_costo = models.GeneratedField(
            expression=F("cantidad") * F("costo_unitario"),
            output_field=DecimalField(max_digits=14, decimal_places=2),
            db_persist=True,
            db_column="total_costo",
        )
    else:
        total_costo = models.DecimalField(
            max_digits=14, decimal_places=2, editable=False, db_column="total_costo"
        )
    referencia = models.TextField(null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "movimiento_inventario"
        managed = MANAGED
        verbose_name = "Movimiento de Inventario"
        verbose_name_plural = "Movimientos de Inventario"
