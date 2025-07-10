from django.urls import path
from . import views
from .views import dashboard_view


urlpatterns = [
    #path('', views.index, name='dashboard'),
    path('', dashboard_view, name='dashboard'),
]
