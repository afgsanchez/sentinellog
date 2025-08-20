from django.contrib import admin
from .models import RegistroAcceso

@admin.register(RegistroAcceso)
class RegistroAccesoAdmin(admin.ModelAdmin):
    list_display = (
        "fecha", "hora_entrada", "matricula", "nombre_apellidos",
        "nombre_empresa", "donde_se_dirigen", "hora_salida",
        "entrega_tarjeta", "devolucion_tarjeta", "tipo"
    )
    list_filter = ("tipo", "fecha", "nombre_empresa", "donde_se_dirigen")
    search_fields = (
        "matricula", "nombre_apellidos", "nombre_empresa",
        "donde_se_dirigen", "entrega_tarjeta", "devolucion_tarjeta"
    )
    ordering = ("-fecha", "-hora_entrada")