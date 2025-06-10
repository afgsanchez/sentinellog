from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='daily_activity_index'),
]
