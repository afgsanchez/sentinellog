from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import DailyReportForm
from .models import DailyReport
import PyPDF2
from django.db.models import Q
from django.shortcuts import get_object_or_404

def index(request):
    reports = DailyReport.objects.all().order_by('-date')

    # Filtros
    report_type = request.GET.get('report_type')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    related_case = request.GET.get('related_case')
    search = request.GET.get('search')

    if report_type:
        reports = reports.filter(report_type=report_type)
    if date_from:
        reports = reports.filter(date__gte=date_from)
    if date_to:
        reports = reports.filter(date__lte=date_to)
    if related_case:
        reports = reports.filter(related_case=related_case)
    if search:
        reports = reports.filter(
            Q(notes__icontains=search) |
            Q(related_case__title__icontains=search) |
            Q(pdf_text__icontains=search)
        )

    # Para el filtro de casos relacionados
    from investigations.models import InvestigationCase
    cases = InvestigationCase.objects.all()

    return render(request, 'daily_reports/index.html', {
        'reports': reports,
        'cases': cases,
        'selected': {
            'report_type': report_type,
            'date_from': date_from,
            'date_to': date_to,
            'related_case': related_case,
            'search': search,
        }
    })



def extract_pdf_text(pdf_file):
    try:
        reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text
    except Exception:
        return ""

@login_required
def add_daily_report(request):
    if request.method == 'POST':
        form = DailyReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.uploaded_by = request.user
            # Extraer texto del PDF
            pdf_file = request.FILES.get('pdf_file')
            if pdf_file:
                report.pdf_text = extract_pdf_text(pdf_file)
            report.save()
            return redirect('daily_reports_index')
    else:
        form = DailyReportForm()
    return render(request, 'daily_reports/add_daily_report.html', {'form': form})

@login_required
def edit_daily_report(request, pk):
    report = get_object_or_404(DailyReport, pk=pk)
    if request.method == 'POST':
        form = DailyReportForm(request.POST, request.FILES, instance=report)
        if form.is_valid():
            report = form.save(commit=False)
            # Si se sube un nuevo PDF, extraer el texto de nuevo
            pdf_file = request.FILES.get('pdf_file')
            if pdf_file:
                report.pdf_text = extract_pdf_text(pdf_file)
            report.save()
            return redirect('daily_reports_index')
    else:
        form = DailyReportForm(instance=report)
    return render(request, 'daily_reports/edit_daily_report.html', {'form': form, 'report': report})