from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from .models import TrakaKeyUser, TrakaKeyUserHistory
from .forms import TrakaKeyUserForm

class TrakaKeyUserListView(ListView):
    model = TrakaKeyUser
    template_name = "traka/user_list.html"
    context_object_name = "users"

    def get_queryset(self):
        queryset = super().get_queryset()
        nombre = self.request.GET.get("nombre")
        sistema = self.request.GET.get("sistema")
        departamento = self.request.GET.get("departamento")
        tipo_llave = self.request.GET.get("tipo_llave")
        activo = self.request.GET.get("activo")

        if nombre:
            queryset = queryset.filter(nombre__icontains=nombre)
        if sistema:
            queryset = queryset.filter(sistema=sistema)
        if departamento:
            queryset = queryset.filter(departamento=departamento)
        if tipo_llave:
            queryset = queryset.filter(tipo_llave=tipo_llave)
        if activo in ["true", "false"]:
            queryset = queryset.filter(activo=(activo == "true"))

        return queryset

class TrakaKeyUserDetailView(DetailView):
    model = TrakaKeyUser
    template_name = "traka/user_detail.html"
    context_object_name = "user"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_history"] = TrakaKeyUserHistory.objects.filter(
            sistema=self.object.sistema,
            posicion=self.object.posicion
        ).order_by("-fecha_cambio")
        return context


class TrakaKeyUserCreateView(CreateView):
    model = TrakaKeyUser
    form_class = TrakaKeyUserForm
    template_name = "traka/user_form.html"
    success_url = reverse_lazy("traka:user_list")

class TrakaKeyUserUpdateView(UpdateView):
    model = TrakaKeyUser
    form_class = TrakaKeyUserForm
    template_name = "traka/user_form.html"
    success_url = reverse_lazy("traka:user_list")
