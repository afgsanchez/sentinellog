from django.urls import path
from . import views

urlpatterns = [
    path('', views.registro_list, name='registro_list'),
    path('importar/', views.registro_import, name='registro_import'),
]