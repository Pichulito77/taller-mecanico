from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
import os

MANAGED = os.getenv("USE_SQLITE", "false").lower() == "true"


class Cliente(models.Model):
    id = models.BigAutoField(db_column="cliente_id", primary_key=True)
    razon_social = models.CharField(max_length=150)
    documento = models.CharField(max_length=50, unique=True, null=True, blank=True)
    email = models.EmailField(max_length=254, null=True, blank=True)
    telefono = models.CharField(max_length=30, null=True, blank=True)
    direccion = models.TextField(null=True, blank=True)
    ciudad = models.CharField(max_length=100, null=True, blank=True)
    provincia = models.CharField(max_length=100, null=True, blank=True)
    codigo_postal = models.CharField(max_length=20, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "cliente"
        managed = MANAGED  # managed externally en PG; gestionado por Django en SQLite
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ["razon_social", "id"]

    def __str__(self) -> str:
        return f"{self.razon_social} ({self.documento or '-'})"


class Vehiculo(models.Model):
    id = models.BigAutoField(db_column="vehiculo_id", primary_key=True)
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.RESTRICT,
        related_name="vehiculos",
        db_column="cliente_id",
    )
    placa = models.CharField(max_length=20, unique=True)
    vin = models.CharField(max_length=50, unique=True, null=True, blank=True)
    marca = models.CharField(max_length=50, null=True, blank=True)
    modelo = models.CharField(max_length=50, null=True, blank=True)
    anio = models.SmallIntegerField(null=True, blank=True)
    color = models.CharField(max_length=30, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "vehiculo"
        managed = MANAGED
        verbose_name = "Vehículo"
        verbose_name_plural = "Vehículos"
        indexes = [
            models.Index(fields=["cliente"], name="idx_vehiculo_cliente_dj"),
        ]

    def clean(self) -> None:
        if self.placa:
            normalized = self.placa.replace(" ", "").upper()
            if not normalized:
                raise ValidationError({"placa": _("La placa no puede quedar vacía")})
            self.placa = normalized

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.placa} — {self.marca or ''} {self.modelo or ''}".strip()
