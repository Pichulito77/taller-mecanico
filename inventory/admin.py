from django.contrib import admin
from .models import Part, InventoryMove


@admin.register(Part)
class PartAdmin(admin.ModelAdmin):
    list_display = ("id", "sku", "nombre", "stock_actual", "stock_minimo", "precio_lista")
    search_fields = ("sku", "nombre")
    list_filter = ("ubicacion",)
    ordering = ("sku",)


@admin.register(InventoryMove)
class InventoryMoveAdmin(admin.ModelAdmin):
    list_display = ("id", "repuesto", "tipo", "cantidad", "costo_unitario", "total_costo", "fecha", "ot_id")
    search_fields = ("repuesto__sku", "repuesto__nombre", "tipo")
    list_filter = ("tipo",)
    ordering = ("-fecha",)