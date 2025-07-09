from django.contrib import admin
from .models import TrakaKeyUser, TrakaKeyUserHistory

@admin.register(TrakaKeyUser)
class TrakaKeyUserAdmin(admin.ModelAdmin):
    list_display = ("nombre", "departamento", "sistema", "posicion", "tipo_llave", "activo")
    list_filter = ("departamento", "sistema", "tipo_llave", "activo")
    search_fields = ("nombre", "cargo")

@admin.register(TrakaKeyUserHistory)
class TrakaKeyUserHistoryAdmin(admin.ModelAdmin):
    list_display = ("sistema", "posicion", "nombre_anterior", "nombre_nuevo", "fecha_cambio")
    list_filter = ("sistema", "fecha_cambio")
    search_fields = ("nombre_anterior", "nombre_nuevo")
