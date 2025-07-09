from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import VisionlineOperator
from .forms import VisionlineOperatorForm
from django.http import FileResponse
from datetime import datetime

def operator_list(request):
    qs = VisionlineOperator.objects.all().order_by('-created_at')

    # Filtros
    estado = request.GET.get('estado')
    search = request.GET.get('search')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')

    if estado in ['activo', 'inactivo']:
        qs = qs.filter(is_active=(estado == 'activo'))

    if search:
        qs = qs.filter(
            Q(full_name__icontains=search) |
            Q(username_assigned__icontains=search) |
            Q(eid__icontains=search)
        )

    if date_from:
        try:
            date_from_obj = datetime.strptime(date_from, "%Y-%m-%d").date()
            qs = qs.filter(request_date__gte=date_from_obj)
        except ValueError:
            pass

    if date_to:
        try:
            date_to_obj = datetime.strptime(date_to, "%Y-%m-%d").date()
            qs = qs.filter(request_date__lte=date_to_obj)
        except ValueError:
            pass

    context = {
        "operators": qs,
        "estado": estado,
        "search": search,
        "date_from": date_from,
        "date_to": date_to,
    }
    return render(request, "visionline/operator_list.html", context)

def operator_create(request):
    if request.method == "POST":
        form = VisionlineOperatorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("visionline_operator_list")
    else:
        form = VisionlineOperatorForm()
    return render(request, "visionline/operator_form.html", {"form": form, "is_edit": False})

def operator_edit(request, pk):
    operator = get_object_or_404(VisionlineOperator, pk=pk)
    if request.method == "POST":
        form = VisionlineOperatorForm(request.POST, request.FILES, instance=operator)
        if form.is_valid():
            form.save()
            return redirect("visionline_operator_list")
    else:
        # Decodifica el password para mostrarlo en el formulario
        import base64
        try:
            decoded = base64.b64decode(operator.password_assigned).decode("utf-8")
        except Exception:
            decoded = ""
        form = VisionlineOperatorForm(instance=operator, initial={"password_assigned": decoded})
    return render(request, "visionline/operator_form.html", {"form": form, "is_edit": True, "operator": operator})

def operator_pdf(request, pk):
    operator = get_object_or_404(VisionlineOperator, pk=pk)
    return FileResponse(operator.request_pdf, as_attachment=True, filename=operator.request_pdf.name.split("/")[-1])

def operator_print(request):
    qs = VisionlineOperator.objects.all().order_by('-created_at')

    # Filtros (igual que en operator_list)
    estado = request.GET.get('estado')
    search = request.GET.get('search')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')

    if estado in ['activo', 'inactivo']:
        qs = qs.filter(is_active=(estado == 'activo'))

    if search:
        qs = qs.filter(
            Q(full_name__icontains=search) |
            Q(username_assigned__icontains=search) |
            Q(eid__icontains=search)
        )

    if date_from:
        try:
            date_from_obj = datetime.strptime(date_from, "%Y-%m-%d").date()
            qs = qs.filter(request_date__gte=date_from_obj)
        except ValueError:
            pass

    if date_to:
        try:
            date_to_obj = datetime.strptime(date_to, "%Y-%m-%d").date()
            qs = qs.filter(request_date__lte=date_to_obj)
        except ValueError:
            pass

    context = {
        "operators": qs,
    }
    return render(request, "visionline/operator_print.html", context)