from django.urls import path
from . import views

app_name = 'lostfound'

urlpatterns = [
    path('', views.LostFoundListView.as_view(), name='list'),
    path('add/', views.LostFoundCreateView.as_view(), name='add'),
    path('<int:pk>/', views.LostFoundDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.LostFoundUpdateView.as_view(), name='edit'),
]