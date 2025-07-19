from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import (
    Proveedor,
    CategoriaProveedor,
    Presupuesto,
    NotificacionInterna,
    AdjuntoPresupuesto,
    HistorialEstadoPresupuesto
)

@admin.register(CategoriaProveedor)
class CategoriaProveedorAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'cif', 'telefono', 'email')
    search_fields = ('nombre', 'cif', 'email')
    list_filter = ('categoria',)

@admin.register(Presupuesto)
class PresupuestoAdmin(SimpleHistoryAdmin):
    list_display = ('numero', 'proveedor', 'estado', 'fecha', 'subtotal', 'creado')
    list_filter = ('estado', 'proveedor', 'fecha')
    search_fields = ('numero', 'proveedor__nombre')
    date_hierarchy = 'fecha'

@admin.register(NotificacionInterna)
class NotificacionInternaAdmin(admin.ModelAdmin):
    list_display = ('mensaje', 'presupuesto', 'leido', 'fecha')
    list_filter = ('leido', 'fecha')
    search_fields = ('mensaje',)

@admin.register(AdjuntoPresupuesto)
class AdjuntoPresupuestoAdmin(admin.ModelAdmin):
    list_display = ('presupuesto', 'descripcion', 'fecha_subida')
    search_fields = ('descripcion',)

@admin.register(HistorialEstadoPresupuesto)
class HistorialEstadoPresupuestoAdmin(admin.ModelAdmin):
    list_display = ('presupuesto', 'estado', 'fecha')
    list_filter = ('estado', 'fecha')
