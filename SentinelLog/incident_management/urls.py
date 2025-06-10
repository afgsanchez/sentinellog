from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='incident_management_index'),
]
