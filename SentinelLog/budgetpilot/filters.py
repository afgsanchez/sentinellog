import django_filters
from .models import Presupuesto, Proveedor

class PresupuestoFilter(django_filters.FilterSet):
    proveedor = django_filters.ModelChoiceFilter(queryset=Proveedor.objects.all(), label='Proveedor')
    estado = django_filters.ChoiceFilter(choices=Presupuesto.ESTADOS, label='Estado')
    fecha = django_filters.DateFromToRangeFilter(label='Rango de fechas')
    subtotal = django_filters.RangeFilter(label='Rango de subtotal (€)')

    class Meta:
        model = Presupuesto
        fields = ['proveedor', 'estado', 'fecha', 'subtotal']
