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