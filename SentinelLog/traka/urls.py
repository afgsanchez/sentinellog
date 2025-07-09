from django.urls import path
from . import views

app_name = "traka"

urlpatterns = [
    path("", views.TrakaKeyUserListView.as_view(), name="user_list"),
    path("nuevo/", views.TrakaKeyUserCreateView.as_view(), name="user_create"),
    path("<int:pk>/", views.TrakaKeyUserDetailView.as_view(), name="user_detail"),
    path("<int:pk>/editar/", views.TrakaKeyUserUpdateView.as_view(), name="user_update"),
]
