from django.urls import path
from . import views
from .views import dashboard_view, generar_codigo_view


urlpatterns = [
    #path('', views.index, name='dashboard'),
    path('', dashboard_view, name='dashboard'),
    path('generar-codigo/', generar_codigo_view, name='generar_codigo'),
]
