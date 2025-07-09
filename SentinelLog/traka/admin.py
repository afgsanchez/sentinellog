from django.contrib import admin
from .models import TrakaKeyUser

@admin.register(TrakaKeyUser)
class TrakaKeyUserAdmin(admin.ModelAdmin):
    list_display = ("nombre", "departamento", "sistema", "posicion", "tipo_llave", "activo")
    list_filter = ("departamento", "sistema", "tipo_llave", "activo")
    search_fields = ("nombre", "cargo")
