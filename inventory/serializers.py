from rest_framework import serializers

from .models import InventoryMove, Part


class PartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Part
        fields = [
            "id",
            "sku",
            "nombre",
            "unidad",
            "ubicacion",
            "precio_lista",
            "stock_actual",
            "stock_minimo",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ("created_at", "updated_at")


class InventoryMoveSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryMove
        fields = [
            "id",
            "repuesto",
            "tipo",
            "cantidad",
            "costo_unitario",
            "total_costo",
            "referencia",
            "ot_id",
            "user_id",
            "fecha",
        ]
        read_only_fields = ("fecha",)
