from django.urls import path
from . import views

urlpatterns = [
    path('', views.operator_list, name='visionline_operator_list'),
    path('nuevo/', views.operator_create, name='visionline_operator_create'),
    path('editar/<int:pk>/', views.operator_edit, name='visionline_operator_edit'),
    path('pdf/<int:pk>/', views.operator_pdf, name='visionline_operator_pdf'),
    path('imprimir/', views.operator_print, name='visionline_operator_print'),
]