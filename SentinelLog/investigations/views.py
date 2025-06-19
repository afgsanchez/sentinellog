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
    cases = InvestigationCase.objects.all().order_by('-created_at')
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



def generate_pdf_report(request, case_id):
    save_path = os.path.join('investigations', 'reports', f'caso_{case_id}_reporte.pdf')
    if os.path.exists(save_path):
        # Devuelve el PDF guardado
        return FileResponse(open(save_path, 'rb'), as_attachment=True, filename=f'caso_{case_id}_reporte.pdf')
    else:
        # Si no existe, genera el PDF como antes (opcional)
        case = InvestigationCase.objects.get(id=case_id)
        conclusiones = case.conclusiones or "No se proporcionaron conclusiones."

        pdf = CyberReportPDF()
        pdf.add_page()
        # Portada
        pdf.set_font("Arial", 'B', 20)
        pdf.set_text_color(0, 51, 102)
        pdf.cell(0, 60, '', ln=True)  # Espacio
        pdf.cell(0, 15, f"{case.title}", ln=True, align='C')
        pdf.set_font("Arial", '', 14)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 10, f"Creado por: {case.created_by.username}", ln=True, align='C')
        pdf.cell(0, 10, f"Fecha de creación: {case.created_at.strftime('%d/%m/%Y %H:%M')}", ln=True, align='C')
        pdf.ln(20)
        pdf.set_font("Arial", 'I', 12)
        pdf.set_text_color(120, 120, 120)
        pdf.cell(0, 10, "No se han incluido datos en el caso. Por favor ingrese datos y guarde los cambios.", ln=True, align='C')
        pdf.add_page()

        response = HttpResponse(pdf.output(dest='S').encode('latin1'), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename=caso_{case_id}_reporte.pdf'
        return response



class CyberReportPDF(FPDF):
    def header(self):
        # Logo (opcional, pon tu ruta de logo si tienes uno)
        logo_path = os.path.join(os.path.dirname(__file__), 'static', 'SentinelLog_logo.png')
        self.image(logo_path, 10, 8, 33)
        self.set_font('Arial', 'B', 18)
        self.set_text_color(30, 30, 30)
        self.cell(0, 12, 'MVC Son Antem | Safety & Security', ln=True, align='C')
        self.set_font('Arial', '', 12)
        self.set_text_color(100, 100, 100)
        self.cell(0, 8, 'Reporte confidencial', ln=True, align='C')
        self.ln(5)
        self.set_draw_color(0, 102, 204)
        self.set_line_width(1)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(8)

    def footer(self):
        self.set_y(-18)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 8, f'Página {self.page_no()}', align='L')
        self.cell(0, 8, f'Generado el: {timezone.localtime(timezone.now()).strftime("%d/%m/%Y %H:%M")}', align='R')
    
    def section_title(self, title):
        self.set_font('Arial', 'B', 14)
        self.set_text_color(0, 102, 204)
        self.cell(0, 10, title, ln=True)
        self.set_text_color(0, 0, 0)
        self.set_font('Arial', '', 12)
        self.ln(2)

    def add_divider(self):
        self.set_draw_color(200, 200, 200)
        self.set_line_width(0.5)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(5)

@require_POST
def save_pdf_report(request, case_id):
    case = InvestigationCase.objects.get(id=case_id)
    conclusiones = request.POST.get("conclusiones", "").strip()

    case.conclusiones = conclusiones
    case.pdf_last_saved = timezone.now()
    case.save()

    pdf = CyberReportPDF()
    pdf.add_page()

    # Portada
    pdf.set_font("Arial", 'B', 20)
    pdf.set_text_color(0, 51, 102)
    pdf.cell(0, 60, '', ln=True)  # Espacio
    pdf.cell(0, 15, f"{case.title}", ln=True, align='C')
    pdf.set_font("Arial", '', 14)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, f"Creado por: {case.created_by.username}", ln=True, align='C')
    pdf.cell(0, 10, f"Fecha de creación: {case.created_at.strftime('%d/%m/%Y %H:%M')}", ln=True, align='C')
    pdf.ln(20)
    pdf.set_font("Arial", 'I', 12)
    pdf.set_text_color(120, 120, 120)
    pdf.cell(0, 10, "Informe generado automáticamente por SentinelLog", ln=True, align='C')
    pdf.add_page()

    # Descripción
    pdf.section_title("1. Descripción del Caso")
    pdf.set_font("Arial", '', 12)
    pdf.multi_cell(0, 8, case.description)
    pdf.add_divider()

    # Documentos Adjuntos
    pdf.section_title("2. Documentos Adjuntos")
    docs = case.documents.all()
    if docs:
        pdf.set_font("Arial", 'B', 11)
        pdf.set_fill_color(230, 230, 250)
        pdf.cell(100, 8, "Archivo", 1, 0, 'C', 1)
        pdf.cell(80, 8, "Descripción", 1, 1, 'C', 1)
        pdf.set_font("Arial", '', 11)
        for doc in docs:
            x = pdf.get_x()
            y = pdf.get_y()
            # Calcula la altura necesaria para la descripción
            desc_width = 80
            desc_lines = pdf.multi_cell(desc_width, 8, doc.description or "-", border=0, align='L', split_only=True)
            desc_height = 8 * len(desc_lines)
            # Archivo (nombre)
            pdf.set_xy(x, y)
            pdf.cell(100, desc_height, doc.file.name.split('/')[-1], border=1)
            # Descripción (multilínea)
            pdf.set_xy(x + 100, y)
            pdf.multi_cell(desc_width, 8, doc.description or "-", border=1)
            pdf.set_y(y + desc_height)
    else:
        pdf.set_font("Arial", 'I', 11)
        pdf.cell(0, 8, "No hay documentos adjuntos.", ln=True)
    pdf.add_divider()

    # Comentarios
    pdf.section_title("3. Comentarios")
    comments = case.comments.all()
    if comments:
        for comment in comments:
            pdf.set_font("Arial", 'B', 11)
            pdf.set_text_color(0, 102, 204)
            pdf.cell(0, 7, f"{comment.author} ({comment.created_at.strftime('%d/%m/%Y %H:%M')})", ln=True)
            pdf.set_font("Arial", '', 11)
            pdf.set_text_color(0, 0, 0)
            pdf.multi_cell(0, 7, comment.comment)
            pdf.ln(2)
    else:
        pdf.set_font("Arial", 'I', 11)
        pdf.cell(0, 8, "No hay comentarios registrados.", ln=True)
    pdf.add_divider()

    # Entrevistas
    pdf.section_title("4. Entrevistas")
    interviews = case.interviews.all()
    if interviews:
        for interview in interviews:
            pdf.set_font("Arial", 'B', 11)
            pdf.set_text_color(0, 102, 204)
            pdf.cell(0, 7, f"{interview.person_name} ({interview.role}) - {interview.date.strftime('%d/%m/%Y')}", ln=True)
            pdf.set_font("Arial", '', 11)
            pdf.set_text_color(0, 0, 0)
            pdf.multi_cell(0, 7, interview.summary)
            pdf.ln(2)
    else:
        pdf.set_font("Arial", 'I', 11)
        pdf.cell(0, 8, "No hay entrevistas registradas.", ln=True)
    pdf.add_divider()

    # Conclusiones
    pdf.section_title("5. Conclusiones")
    pdf.set_font("Arial", 'B', 12)
    pdf.set_text_color(0, 0, 0)  # Rojo Bootstrap
    pdf.multi_cell(0, 10, conclusiones or "No se proporcionaron conclusiones.")
    pdf.set_text_color(0, 0, 0)

    # Guardar PDF
    save_path = os.path.join('investigations', 'reports', f'caso_{case.id}_reporte.pdf')
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    pdf.output(save_path)

    messages.success(request, "El archivo PDF ha sido guardado exitosamente.")
    return redirect('case_detail', case_id=case_id)