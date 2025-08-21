from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import InventoryMove, Part


class LowStockFilter(admin.SimpleListFilter):
    title = _("Stock bajo")
    parameter_name = "low_stock"

    def lookups(self, request, model_admin):
        return (("1", _("Solo bajo stock")),)

    def queryset(self, request, queryset):
        if self.value() == "1":
            return queryset.filter(stock_actual__lt=admin.models.F("stock_minimo"))
        return queryset


@admin.register(Part)
class PartAdmin(admin.ModelAdmin):
    list_display = ("id", "sku", "nombre", "stock_actual", "stock_minimo", "precio_lista")
    search_fields = ("sku", "nombre")
    list_filter = ("ubicacion", LowStockFilter)
    ordering = ("sku",)
    list_editable = ("stock_minimo", "precio_lista")

    def get_model_perms(self, request):
        if not request.user.is_superuser:
            return {}
        return super().get_model_perms(request)


@admin.register(InventoryMove)
class InventoryMoveAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "repuesto",
        "tipo",
        "cantidad",
        "costo_unitario",
        "total_costo",
        "fecha",
        "ot_id",
    )
    search_fields = ("repuesto__sku", "repuesto__nombre", "tipo")
    list_filter = ("tipo",)
    ordering = ("-fecha",)

    def get_model_perms(self, request):
        if not request.user.is_superuser:
            return {}
        return super().get_model_perms(request)
