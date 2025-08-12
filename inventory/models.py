from django.db import models


class Part(models.Model):
    id = models.BigAutoField(db_column="repuesto_id", primary_key=True)
    sku = models.CharField(max_length=60, unique=True)
    nombre = models.CharField(max_length=150)
    unidad = models.CharField(max_length=20, default="unidad")
    ubicacion = models.CharField(max_length=100, null=True, blank=True)
    precio_lista = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    stock_actual = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    stock_minimo = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "repuesto"
        managed = False
        verbose_name = "Repuesto"
        verbose_name_plural = "Repuestos"
        ordering = ["sku"]

    def __str__(self) -> str:
        return f"{self.sku} — {self.nombre}"


class InventoryMove(models.Model):
    id = models.BigAutoField(db_column="movimiento_id", primary_key=True)
    repuesto = models.ForeignKey(Part, on_delete=models.RESTRICT, db_column="repuesto_id")
    tipo = models.CharField(max_length=10)  # entrada, salida, ajuste
    cantidad = models.DecimalField(max_digits=12, decimal_places=3)
    costo_unitario = models.DecimalField(max_digits=12, decimal_places=2)
    total_costo = models.DecimalField(max_digits=14, decimal_places=2)
    referencia = models.TextField(null=True, blank=True)
    ot_id = models.BigIntegerField(null=True, blank=True)
    user_id = models.BigIntegerField(null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "movimiento_inventario"
        managed = False
        verbose_name = "Movimiento de Inventario"
        verbose_name_plural = "Movimientos de Inventario"
        ordering = ["-fecha"]

    def __str__(self) -> str:
        return f"{self.tipo} {self.cantidad} de {self.repuesto_id}"