from django.contrib import admin
from .models import Cliente, Vehiculo


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("id", "razon_social", "documento", "email", "telefono", "created_at")
    search_fields = ("razon_social", "documento", "email")
    list_filter = ("ciudad", "provincia")
    ordering = ("razon_social",)


@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ("id", "placa", "vin", "cliente", "marca", "modelo", "anio", "created_at")
    search_fields = ("placa", "vin", "marca", "modelo", "cliente__razon_social")
    list_filter = ("marca", "anio")
    autocomplete_fields = ("cliente",)
    ordering = ("placa",)