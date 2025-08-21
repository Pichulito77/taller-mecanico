from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import WorkOrder, WorkOrderItem


@admin.register(WorkOrder)
class WorkOrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "numero",
        "cliente",
        "vehiculo",
        "estado",
        "total",
        "fecha_apertura",
        "acciones",
    )
    search_fields = ("numero", "cliente__razon_social", "vehiculo__placa")
    list_filter = ("estado",)
    ordering = ("-id",)
    list_editable = ("estado",)
    exclude = ("asignado_a_user_id",)
    readonly_fields = ("fecha_apertura",)
    fieldsets = (
        (None, {"fields": ("numero", "cliente", "vehiculo", "estado")}),
        (
            "Fechas",
            {"fields": ("fecha_ingreso", "fecha_salida", "fecha_cierre", "fecha_apertura")},
        ),
        ("Vehículo", {"fields": ("matricula", "color", "kilometraje", "ingresado_en_grua")}),
        ("Detalles", {"fields": ("diagnostico", "notas", "datos_adicionales")}),
        ("Totales", {"fields": ("subtotal", "impuestos", "descuento", "total")}),
    )

    actions = ("finalizar_seleccionadas",)

    def acciones(self, obj: WorkOrder):
        url_print = reverse("print_ot", args=[obj.id])
        url_pdf = reverse("pdf_ot", args=[obj.id])
        btn = (
            'style="display:inline-block;margin-right:6px;padding:6px 10px;'
            'border-radius:10px;border:1px solid #cbd5e1;text-decoration:none"'
        )
        return format_html(
            f'<a {btn} href="{{}}" target="_blank">Imprimir</a>'
            f'<a {btn} href="{{}}" target="_blank">PDF</a>',
            url_print,
            url_pdf,
        )

    def finalizar_seleccionadas(self, request, queryset):
        updated = queryset.update(estado="finalizada")
        self.message_user(request, f"{updated} OTs finalizadas")

    finalizar_seleccionadas.short_description = "Finalizar OTs seleccionadas"


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

    def get_model_perms(self, request):
        if not request.user.is_superuser:
            return {}
        return super().get_model_perms(request)
