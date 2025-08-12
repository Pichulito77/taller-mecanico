from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models import F, DecimalField
try:
    # Django 5+: GeneratedField available
    from django.db.models import GeneratedField  # type: ignore
except Exception:  # pragma: no cover
    GeneratedField = None  # fallback for older versions

from customers.models import Cliente, Vehiculo


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

    ESTADOS = (
        ("creada", "Creada"),
        ("diagnostico", "Diagnóstico"),
        ("en_proceso", "En proceso"),
        ("en_espera", "En espera"),
        ("finalizada", "Finalizada"),
        ("entregada", "Entregada"),
        ("cancelada", "Cancelada"),
    )
    estado = models.CharField(max_length=20, choices=ESTADOS, default="creada")

    diagnostico = models.TextField(null=True, blank=True)
    notas = models.TextField(null=True, blank=True)

    fecha_apertura = models.DateTimeField(auto_now_add=True)
    fecha_cierre = models.DateTimeField(null=True, blank=True)

    subtotal = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    impuestos = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    descuento = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "orden_trabajo"
        managed = False
        verbose_name = "Orden de Trabajo"
        verbose_name_plural = "Órdenes de Trabajo"
        indexes = [
            models.Index(fields=["estado"], name="idx_ot_estado_dj"),
            models.Index(fields=["vehiculo"], name="idx_ot_vehiculo_dj"),
        ]

    def __str__(self) -> str:
        return f"OT {self.numero} — {self.estado}"

    def clean(self) -> None:
        if not self.asignado_a_user_id or self.asignado_a_user_id == 0:
            self.asignado_a_user_id = None

    @staticmethod
    def is_valid_transition(old: str, new: str) -> bool:
        allowed = {
            "creada": {"diagnostico", "cancelada", "finalizada"},
            "diagnostico": {"en_proceso", "en_espera", "cancelada", "finalizada"},
            "en_proceso": {"en_espera", "finalizada", "cancelada"},
            "en_espera": {"en_proceso", "cancelada", "finalizada"},
            "finalizada": {"entregada"},
            "entregada": set(),
            "cancelada": set(),
        }
        return new in allowed.get(old, set())


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
    if GeneratedField:
        total = GeneratedField(
            expression=F("cantidad") * F("precio_unitario") + F("impuestos"),
            output_field=DecimalField(max_digits=14, decimal_places=2),
            db_persist=True,
            db_column="total",
        )
    else:
        # Fallback: treat as read-only DecimalField; DB will compute it
        total = models.DecimalField(
            max_digits=14, decimal_places=2, editable=False, db_column="total"
        )

    class Meta:
        db_table = "ot_item"
        managed = False
        verbose_name = "Ítem de OT"
        verbose_name_plural = "Ítems de OT"
        indexes = [models.Index(fields=["workorder"], name="idx_ot_item_ot_dj")]

    def clean(self) -> None:
        if self.tipo == "repuesto" and not self.repuesto_id:
            raise ValidationError({"repuesto_id": _("Requiere repuesto si el tipo es repuesto")})
        if self.cantidad is not None and self.cantidad <= 0:
            raise ValidationError({"cantidad": _("La cantidad debe ser > 0")})
        if self.precio_unitario is not None and self.precio_unitario < 0:
            raise ValidationError({"precio_unitario": _("El precio no puede ser negativo")})

    def save(self, *args, **kwargs):
        self.full_clean()
        # Asegurar que no se envía valor para total (DB lo genera)
        if hasattr(self, "total"):
            try:
                delattr(self, "total")
            except Exception:
                pass
        return super().save(*args, **kwargs)