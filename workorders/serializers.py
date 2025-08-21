from decimal import Decimal

from django.db import transaction
from rest_framework import serializers

from .models import WorkOrder, WorkOrderItem
from .services import finalize_workorder_and_deduct_inventory


def recalc_totals(ot: WorkOrder) -> None:
    subtotal = Decimal("0")
    impuestos = Decimal("0")
    for it in WorkOrderItem.objects.filter(workorder=ot):
        subtotal += (it.cantidad or 0) * (it.precio_unitario or 0)
        impuestos += it.impuestos or 0
    ot.subtotal = subtotal
    ot.impuestos = impuestos
    ot.total = subtotal + impuestos - (ot.descuento or 0)
    ot.save(update_fields=["subtotal", "impuestos", "total", "updated_at"])


class WorkOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkOrder
        fields = [
            "id",
            "numero",
            "cliente",
            "vehiculo",
            "asignado_a_user_id",
            "estado",
            "diagnostico",
            "notas",
            "fecha_ingreso",
            "fecha_salida",
            "matricula",
            "color",
            "kilometraje",
            "ingresado_en_grua",
            "datos_adicionales",
            "fecha_apertura",
            "fecha_cierre",
            "subtotal",
            "impuestos",
            "descuento",
            "total",
            "created_at",
            "updated_at",
        ]
        read_only_fields = (
            "subtotal",
            "impuestos",
            "total",
            "fecha_apertura",
            "fecha_cierre",
            "created_at",
            "updated_at",
        )

    def validate_estado(self, value: str) -> str:
        instance: WorkOrder | None = self.instance
        if (
            instance
            and value != instance.estado
            and not WorkOrder.is_valid_transition(instance.estado, value)
        ):
            raise serializers.ValidationError("Transición de estado inválida")
        return value

    @transaction.atomic
    def update(self, instance, validated_data):
        estado_nuevo = validated_data.get("estado")
        if estado_nuevo == "finalizada" and instance.estado != "finalizada":
            # Validar y descontar inventario
            finalize_workorder_and_deduct_inventory(instance, user_id=instance.asignado_a_user_id)
            # Recalcular totales después por si hay cambios
            recalc_totals(instance)
            # Merge otros cambios si los hay (diagnóstico/notas)
            for k, v in validated_data.items():
                if k != "estado":
                    setattr(instance, k, v)
            instance.save()
            return instance
        obj = super().update(instance, validated_data)
        return obj


class WorkOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkOrderItem
        fields = [
            "id",
            "workorder",
            "tipo",
            "repuesto_id",
            "descripcion",
            "cantidad",
            "precio_unitario",
            "impuestos",
            "total",
        ]
        read_only_fields = ("total",)

    @transaction.atomic
    def create(self, validated_data):
        item = super().create(validated_data)
        recalc_totals(item.workorder)
        return item

    @transaction.atomic
    def update(self, instance, validated_data):
        item = super().update(instance, validated_data)
        recalc_totals(item.workorder)
        return item

    @transaction.atomic
    def delete(self):
        ot = self.instance.workorder
        super().delete()
        recalc_totals(ot)
