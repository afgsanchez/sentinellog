from django.urls import path
from . import views

app_name = 'budgetpilot'

urlpatterns = [
    path('', views.PresupuestoListView.as_view(), name='presupuesto_list'),
    path('presupuesto/<int:pk>/', views.PresupuestoDetailView.as_view(), name='presupuesto_detail'),
    path('presupuesto/nuevo/', views.PresupuestoCreateView.as_view(), name='presupuesto_create'),
    path('presupuesto/<int:pk>/editar/', views.PresupuestoUpdateView.as_view(), name='presupuesto_edit'),
    path('proveedor/nuevo/', views.ProveedorCreateView.as_view(), name='proveedor_create'),
    path('categoria/nueva/', views.CategoriaProveedorCreateView.as_view(), name='categoria_create'),
]
