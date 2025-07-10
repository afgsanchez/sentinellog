from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from .models import TrakaKeyUser, TrakaKeyUserHistory
from .forms import TrakaKeyUserForm
from datetime import date
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
import io


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

    def form_valid(self, form):
        instance = form.save(commit=False)
        original = self.get_object()

        # Si el nombre se ha borrado (posición liberada)
        if original.nombre and not instance.nombre:
            TrakaKeyUserHistory.objects.create(
                sistema=original.sistema,
                posicion=original.posicion,
                nombre_anterior=original.nombre,
                nombre_nuevo="(libre)"
            )
            instance.fecha_desasignacion = date.today()
            instance.activo = False

        # Si el nombre ha cambiado (reasignación)
        elif original.nombre != instance.nombre:
            TrakaKeyUserHistory.objects.create(
                sistema=original.sistema,
                posicion=original.posicion,
                nombre_anterior=original.nombre,
                nombre_nuevo=instance.nombre
            )
            instance.fecha_desasignacion = None
            instance.activo = True

        instance.save()
        form.save_m2m()
        return super().form_valid(form)




def generar_checklist_pdf(request):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 14)
    c.drawString(2 * cm, height - 2 * cm, "Checklist de Auditoría de Llaves Traka")

    headers = ["Sistema", "Posición", "Tipo", "Estado", "Nombre asignado", "Anotaciones"]
    col_positions = [2, 5, 7, 9, 11, 15]  # en cm

    c.setFont("Helvetica-Bold", 10)
    y = height - 3 * cm
    for i, header in enumerate(headers):
        c.drawString(col_positions[i] * cm, y, header)

    c.setFont("Helvetica", 9)
    y -= 0.7 * cm
    line_height = 0.6 * cm

    keys = TrakaKeyUser.objects.all().order_by("sistema", "posicion")

    for key in keys:
        if y < 2 * cm:
            c.showPage()
            y = height - 2 * cm
            c.setFont("Helvetica-Bold", 10)
            for i, header in enumerate(headers):
                c.drawString(col_positions[i] * cm, y, header)
            y -= 0.7 * cm
            c.setFont("Helvetica", 9)

        estado = "Ocupada" if key.activo else "Libre"
        values = [
            key.sistema,
            str(key.posicion),
            key.tipo_llave,
            estado,
            key.nombre,
            "__________________________"
        ]
        for i, value in enumerate(values):
            c.drawString(col_positions[i] * cm, y, value)
        y -= line_height

    c.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename="auditoria_traka.pdf")
