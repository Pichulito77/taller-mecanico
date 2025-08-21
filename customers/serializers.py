from rest_framework import serializers

from .models import Cliente, Vehiculo


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = [
            "id",
            "razon_social",
            "documento",
            "email",
            "telefono",
            "direccion",
            "ciudad",
            "provincia",
            "codigo_postal",
            "notes",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ("created_at", "updated_at")


class VehiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehiculo
        fields = [
            "id",
            "cliente",
            "placa",
            "vin",
            "marca",
            "modelo",
            "anio",
            "color",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ("created_at", "updated_at")

    def validate(self, attrs):
        placa = attrs.get("placa")
        if placa:
            attrs["placa"] = placa.replace(" ", "").upper()
        return attrs
