from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_daily_report, name='add_daily_report'),
    path('edit/<int:pk>/', views.edit_daily_report, name='edit_daily_report'),
    path('', views.index, name='daily_reports_index'),
]