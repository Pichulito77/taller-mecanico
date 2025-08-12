from django.contrib import admin
from .models import Quote, QuoteItem, Invoice, InvoiceItem


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ("id", "numero", "cliente", "vehiculo", "estado", "total", "fecha_emision")
    search_fields = ("numero", "cliente__razon_social")
    list_filter = ("estado",)
    ordering = ("-id",)
    exclude = ("creado_por_user_id",)


@admin.register(QuoteItem)
class QuoteItemAdmin(admin.ModelAdmin):
    list_display = ("id", "presupuesto", "tipo", "descripcion", "cantidad", "precio_unitario", "total")
    search_fields = ("descripcion",)
    list_filter = ("tipo",)


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("id", "numero", "cliente", "vehiculo", "estado", "total", "fecha_emision")
    search_fields = ("numero", "cliente__razon_social")
    list_filter = ("estado",)
    ordering = ("-id",)


@admin.register(InvoiceItem)
class InvoiceItemAdmin(admin.ModelAdmin):
    list_display = ("id", "factura", "tipo", "descripcion", "cantidad", "precio_unitario", "total")
    search_fields = ("descripcion",)
    list_filter = ("tipo",)