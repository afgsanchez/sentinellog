import os
from datetime import timezone
from django.utils import timezone
from django.utils.timezone import localtime
from django.views.decorators.http import require_POST
from fpdf import FPDF
from django.contrib import messages
from django.http import HttpResponse, FileResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import InvestigationCase, InvestigationDocument, InvestigationComment, InterviewRecord
from .forms import (
    InvestigationCaseForm,
    InvestigationDocumentForm,
    InvestigationCommentForm,
    InterviewRecordForm
)

def index(request):
    cases = InvestigationCase.objects.all()
    return render(request, 'investigations/index.html', {'cases': cases})

def case_detail(request, case_id):
    case = get_object_or_404(InvestigationCase, id=case_id)
    documents = case.documents.all()
    comments = case.comments.all()
    interviews = case.interviews.all()
    return render(request, 'investigations/case_detail.html', {
        'case': case,
        'documents': documents,
        'comments': comments,
        'interviews': interviews
    })

def add_case(request):
    if request.method == 'POST':
        form = InvestigationCaseForm(request.POST)
        if form.is_valid():
            case = form.save(commit=False)
            case.created_by = request.user
            case.save()
            return redirect('investigations_index')
    else:
        form = InvestigationCaseForm()
    return render(request, 'investigations/add_case.html', {'form': form})



@require_POST
def toggle_case_status(request, case_id):
    case = get_object_or_404(InvestigationCase, id=case_id)
    # Cambia el estado según el checkbox
    case.is_closed = bool(request.POST.get('is_closed'))
    case.save()
    return redirect('case_detail', case_id=case_id)


def add_document(request, case_id):
    case = get_object_or_404(InvestigationCase, id=case_id)
    if request.method == 'POST':
        form = InvestigationDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.case = case
            document.uploaded_by = request.user
            document.save()
            return redirect('case_detail', case_id=case.id)
    else:
        form = InvestigationDocumentForm()
    return render(request, 'investigations/add_document.html', {'form': form, 'case': case})

def add_comment(request, case_id):
    case = get_object_or_404(InvestigationCase, id=case_id)
    if request.method == 'POST':
        form = InvestigationCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.case = case
            comment.author = request.user
            comment.save()
            return redirect('case_detail', case_id=case.id)
    else:
        form = InvestigationCommentForm()
    return render(request, 'investigations/add_comment.html', {'form': form, 'case': case})

def add_interview(request, case_id):
    case = get_object_or_404(InvestigationCase, id=case_id)
    if request.method == 'POST':
        form = InterviewRecordForm(request.POST)
        if form.is_valid():
            interview = form.save(commit=False)
            interview.case = case
            interview.conducted_by = request.user
            interview.save()
            return redirect('case_detail', case_id=case.id)
    else:
        form = InterviewRecordForm()
    return render(request, 'investigations/add_interview.html', {'form': form, 'case': case})


from django.utils.timezone import localtime

# def generate_pdf_report(request, case_id):
#     case = InvestigationCase.objects.get(id=case_id)
#     conclusiones = case.conclusiones or "No se proporcionaron conclusiones."

#     pdf = FPDF()
#     pdf.add_page()
#     pdf.set_font("Arial", 'B', 16)
#     pdf.cell(0, 10, "Reporte de Caso de Investigación", ln=True, align='C')

#     pdf.set_font("Arial", 'B', 12)
#     pdf.cell(0, 10, f"Título: {case.title}", ln=True)
#     pdf.set_font("Arial", '', 12)
#     pdf.multi_cell(0, 10, f"Descripción: {case.description}")

#     pdf.ln(5)
#     pdf.set_font("Arial", 'B', 12)
#     pdf.cell(0, 10, "Documentos Adjuntos:", ln=True)
#     for doc in case.documents.all():
#         pdf.set_font("Arial", '', 12)
#         pdf.cell(0, 10, f"- {doc.description or doc.file.name}", ln=True)

#     pdf.ln(5)
#     pdf.set_font("Arial", 'B', 12)
#     pdf.cell(0, 10, "Comentarios:", ln=True)
#     for comment in case.comments.all():
#         pdf.set_font("Arial", '', 12)
#         pdf.multi_cell(0, 10, f"{comment.author} ({comment.created_at}): {comment.comment}")

#     pdf.ln(5)
#     pdf.set_font("Arial", 'B', 12)
#     pdf.cell(0, 10, "Entrevistas:", ln=True)
#     for interview in case.interviews.all():
#         pdf.set_font("Arial", '', 12)
#         pdf.multi_cell(0, 10, f"{interview.person_name} ({interview.role}) - {interview.date}:\n{interview.summary}")

#     pdf.ln(5)
#     pdf.set_font("Arial", 'B', 12)
#     pdf.cell(0, 10, "Conclusiones:", ln=True)
#     pdf.set_font("Arial", '', 12)
#     pdf.multi_cell(0, 10, conclusiones)

#     # Fecha de generación
#     if case.pdf_last_saved:
#         pdf.ln(10)
#         pdf.set_font("Arial", 'I', 10)
#         pdf.cell(0, 10, f"PDF generado el: {localtime(case.pdf_last_saved).strftime('%d/%m/%Y %H:%M')}", ln=True)

#     response = HttpResponse(pdf.output(dest='S').encode('latin1'), content_type='application/pdf')
#     response['Content-Disposition'] = f'attachment; filename=caso_{case.id}_reporte.pdf'
#     return response

def generate_pdf_report(request, case_id):
    save_path = os.path.join('investigations', 'reports', f'caso_{case_id}_reporte.pdf')
    if os.path.exists(save_path):
        # Devuelve el PDF guardado
        return FileResponse(open(save_path, 'rb'), as_attachment=True, filename=f'caso_{case_id}_reporte.pdf')
    else:
        # Si no existe, genera el PDF como antes (opcional)
        case = InvestigationCase.objects.get(id=case_id)
        conclusiones = case.conclusiones or "No se proporcionaron conclusiones."

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, "Reporte de Caso de Investigación", ln=True, align='C')
        # ...el resto de tu código para generar el PDF...
        response = HttpResponse(pdf.output(dest='S').encode('latin1'), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename=caso_{case_id}_reporte.pdf'
        return response


@require_POST
def save_pdf_report(request, case_id):
    case = InvestigationCase.objects.get(id=case_id)
    conclusiones = request.POST.get("conclusiones", "").strip()

    # Guardar en la base de datos
    case.conclusiones = conclusiones
    case.pdf_last_saved = timezone.now()
    case.save()


    # Mostrar mensaje según si hay conclusiones o no
    if conclusiones:
        messages.success(request, "El archivo PDF ha sido guardado exitosamente con las conclusiones.")
    else:
        messages.info(request, "El archivo PDF ha sido guardado. Puedes añadir las conclusiones más adelante.")

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Reporte de Caso de Investigación", ln=True, align='C')

    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, f"Título: {case.title}", ln=True)
    pdf.set_font("Arial", '', 12)
    pdf.multi_cell(0, 10, f"Descripción: {case.description}")

    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Documentos Adjuntos:", ln=True)
    for doc in case.documents.all():
        pdf.set_font("Arial", '', 12)
        pdf.cell(0, 10, f"- {doc.description or doc.file.name}", ln=True)

    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Comentarios:", ln=True)
    for comment in case.comments.all():
        pdf.set_font("Arial", '', 12)
        pdf.multi_cell(0, 10, f"{comment.author} ({comment.created_at}): {comment.comment}")

    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Entrevistas:", ln=True)
    for interview in case.interviews.all():
        pdf.set_font("Arial", '', 12)
        pdf.multi_cell(0, 10, f"{interview.person_name} ({interview.role}) - {interview.date}:\n{interview.summary}")

    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Conclusiones:", ln=True)
    pdf.set_font("Arial", '', 12)
    pdf.multi_cell(0, 10, conclusiones or "No se proporcionaron conclusiones.")

    # Añadir la fecha de guardado al final del PDF
    pdf.ln(10)
    pdf.set_font("Arial", 'I', 10)
    pdf.cell(0, 10, f"PDF generado el: {localtime(case.pdf_last_saved).strftime('%d/%m/%Y %H:%M')}", ln=True)

    save_path = os.path.join('investigations', 'reports', f'caso_{case.id}_reporte.pdf')
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    pdf.output(save_path)


    messages.success(request, "El archivo PDF ha sido guardado exitosamente.")
    return redirect('case_detail', case_id=case_id)
