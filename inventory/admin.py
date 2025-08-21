from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import InventoryMove, Part


@admin.register(Part)
class PartAdmin(admin.ModelAdmin):
    list_display = ("id", "sku", "nombre", "costo_unitario")
    search_fields = ("sku", "nombre")
    ordering = ("sku",)

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
    )
    search_fields = ("repuesto__sku", "repuesto__nombre", "tipo")
    list_filter = ("tipo",)
    ordering = ("-fecha",)

    def get_model_perms(self, request):
        if not request.user.is_superuser:
            return {}
        return super().get_model_perms(request)
