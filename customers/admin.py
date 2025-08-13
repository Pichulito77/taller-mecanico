from django.contrib import admin
from .models import Cliente, Vehiculo


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
	list_display = ("id", "razon_social", "documento", "email", "telefono", "created_at")
	search_fields = ("razon_social", "documento", "email")
	list_filter = ("ciudad", "provincia")
	ordering = ("razon_social",)
	fieldsets = (
		(None, {"fields": ("razon_social", "documento", "email", "telefono")}),
		("Dirección", {"fields": ("direccion", "ciudad", "provincia")}),
	)
	def get_form(self, request, obj=None, **kwargs):
		form = super().get_form(request, obj, **kwargs)
		if "documento" in form.base_fields:
			form.base_fields["documento"].help_text = "CUIT/DNI del cliente"
		return form


@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
	list_display = ("id", "placa", "vin", "cliente", "marca", "modelo", "anio", "created_at")
	search_fields = ("placa", "vin", "marca", "modelo", "cliente__razon_social")
	list_filter = ("marca", "anio")
	autocomplete_fields = ("cliente",)
	ordering = ("placa",)
	def get_form(self, request, obj=None, **kwargs):
		form = super().get_form(request, obj, **kwargs)
		if "placa" in form.base_fields:
			form.base_fields["placa"].help_text = "En MAYÚSCULAS, sin espacios"
		return form