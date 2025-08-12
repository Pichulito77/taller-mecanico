from django.contrib import admin
from .models import WorkOrder, WorkOrderItem


@admin.register(WorkOrder)
class WorkOrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "numero",
        "cliente",
        "vehiculo",
        "estado",
        "asignado_a_user_id",
        "total",
        "fecha_apertura",
    )
    search_fields = ("numero", "cliente__razon_social", "vehiculo__placa")
    list_filter = ("estado",)
    ordering = ("-id",)
    # Evitar que el admin intente setear un ID inexistente en tabla app_user
    exclude = ("asignado_a_user_id",)
    fieldsets = (
        (None, {
            "fields": ("numero", "cliente", "vehiculo", "estado")
        }),
        ("Fechas", {
            "fields": ("fecha_ingreso", "fecha_salida", "fecha_apertura", "fecha_cierre")
        }),
        ("Vehículo", {
            "fields": ("matricula", "color", "kilometraje", "ingresado_en_grua")
        }),
        ("Detalles", {
            "fields": ("diagnostico", "notas", "datos_adicionales")
        }),
        ("Totales", {
            "fields": ("subtotal", "impuestos", "descuento", "total")
        }),
    )


@admin.register(WorkOrderItem)
class WorkOrderItemAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "workorder",
        "tipo",
        "descripcion",
        "cantidad",
        "precio_unitario",
        "total",
    )
    search_fields = ("descripcion",)
    list_filter = ("tipo",)
    autocomplete_fields = ("workorder",)