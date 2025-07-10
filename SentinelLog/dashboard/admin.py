from django.contrib import admin
from .models import GrupoTraka
from datetime import date, timedelta
from django.utils.html import format_html

@admin.register(GrupoTraka)
class GrupoTrakaAdmin(admin.ModelAdmin):
    list_display = ('tipo_tarjeta', 'localizacion_tarjeta', 'fecha_caducidad', 'estado_coloreado')
    list_filter = ('fecha_caducidad',)
    search_fields = ('tipo_tarjeta', 'localizacion_tarjeta')

    def estado_coloreado(self, obj):
        hoy = date.today()
        if obj.fecha_caducidad < hoy:
            color = 'red'
            estado = 'Caducado'
        elif obj.fecha_caducidad <= hoy + timedelta(days=2):
            color = 'orange'
            estado = 'Próximo a caducar'
        else:
            color = 'green'
            estado = 'Vigente'
        return format_html('<span style="color: {};">{}</span>', color, estado)

    estado_coloreado.short_description = 'Estado'
