from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from .models import Presupuesto, Proveedor, CategoriaProveedor, HistorialEstadoPresupuesto
from .forms import PresupuestoForm, ProveedorForm, CategoriaProveedorForm
from django_filters.views import FilterView
from .filters import PresupuestoFilter
from django.shortcuts import render, get_object_or_404
from simple_history.utils import update_change_reason
from simple_history.models import HistoricalRecords
from django.utils.timezone import localtime
from datetime import timedelta
from django.utils import timezone
from django.db import models




# Listado de presupuestos
class PresupuestoListView(FilterView):
    model = Presupuesto
    template_name = 'budgetpilot/presupuesto_list.html'
    context_object_name = 'presupuestos'
    filterset_class = PresupuestoFilter
    ordering = ['-estado', '-fecha']
    paginate_by = 10  # Mostrar 5 presupuestos por página


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.get_filterset(self.get_filterset_class())

        hoy = timezone.now()
        cinco_dias = hoy - timedelta(days=5)

        alertas = []

        for presupuesto in Presupuesto.objects.all():
            ultimo_estado = presupuesto.historial_estados.order_by('-fecha').first()

            if ultimo_estado:
                dias_en_estado = (hoy - ultimo_estado.fecha).days

                if (
                    (presupuesto.estado == 'pendiente_aprobacion' and dias_en_estado > 5) or
                    (presupuesto.estado == 'aprobado' and dias_en_estado > 5)
                ):
                    presupuesto.dias_en_estado = dias_en_estado
                    alertas.append(presupuesto)

            if presupuesto.fecha_entrega_estimada and presupuesto.fecha_entrega_estimada < hoy.date():
                if presupuesto not in alertas:
                    presupuesto.dias_en_estado = None  # No aplica
                    alertas.append(presupuesto)


        context['alertas'] = alertas
        return context





# Detalle de un presupuesto con historial de estados
class PresupuestoDetailView(DetailView):
    model = Presupuesto
    template_name = 'budgetpilot/presupuesto_detail.html'
    context_object_name = 'presupuesto'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        presupuesto = self.get_object()

        # Historial de estados personalizados
        context['historial'] = presupuesto.historial_estados.all().order_by('-fecha')

        # Historial completo con diferencias campo a campo
        historial_simple = []
        history = presupuesto.history.all().order_by('-history_date')
        for i, entry in enumerate(history):
            changes = []
            if i + 1 < len(history):
                previous = history[i + 1]
                for field in presupuesto._meta.fields:
                    field_name = field.name
                    old = getattr(previous, field_name, None)
                    new = getattr(entry, field_name, None)
                    if old != new:
                        changes.append({
                            'campo': field.verbose_name.title(),
                            'antes': old,
                            'despues': new
                        })
            historial_simple.append({
                'usuario': entry.history_user,
                'fecha': localtime(entry.history_date),
                'tipo': entry.get_history_type_display(),
                'cambios': changes
            })

        context['historial_simple'] = historial_simple
        return context



# Crear nuevo presupuesto
class PresupuestoCreateView(CreateView):
    model = Presupuesto
    form_class = PresupuestoForm
    template_name = 'budgetpilot/presupuesto_form.html'
    success_url = reverse_lazy('budgetpilot:presupuesto_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['proveedor_form'] = ProveedorForm()
        return context

class PresupuestoUpdateView(UpdateView):
    model = Presupuesto
    form_class = PresupuestoForm
    template_name = 'budgetpilot/presupuesto_form.html'
    success_url = reverse_lazy('budgetpilot:presupuesto_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['proveedor_form'] = ProveedorForm()
        return context


# Editar presupuesto
class PresupuestoUpdateView(UpdateView):
    model = Presupuesto
    form_class = PresupuestoForm
    template_name = 'budgetpilot/presupuesto_form.html'
    success_url = reverse_lazy('budgetpilot:presupuesto_list')

# Crear proveedor
class ProveedorCreateView(CreateView):
    model = Proveedor
    form_class = ProveedorForm
    template_name = 'budgetpilot/proveedor_form.html'
    success_url = reverse_lazy('budgetpilot:presupuesto_create')

# Crear categoría de proveedor
class CategoriaProveedorCreateView(CreateView):
    model = CategoriaProveedor
    form_class = CategoriaProveedorForm
    template_name = 'budgetpilot/categoria_form.html'
    success_url = reverse_lazy('budgetpilot:presupuesto_create')
