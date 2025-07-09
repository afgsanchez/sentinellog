from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='incident_management_index'),
    path('add/', views.add_incident, name='add_incident'),
    path('edit/<int:pk>/', views.edit_incident, name='edit_incident'),
    path('detail/<int:pk>/', views.incident_detail, name='incident_detail'),
    path('pdf/<int:pk>/', views.generate_incident_pdf, name='generate_incident_pdf'),
    # path('test_pdf/', views.test_pdf, name='test_pdf'),
]