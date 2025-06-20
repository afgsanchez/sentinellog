from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import DailyReportForm
from .models import DailyReport

from django.db.models import Q

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
            Q(related_case__title__icontains=search)
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


@login_required
def add_daily_report(request):
    if request.method == 'POST':
        form = DailyReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.uploaded_by = request.user
            report.save()
            return redirect('daily_reports_index')
    else:
        form = DailyReportForm()
    return render(request, 'daily_reports/add_daily_report.html', {'form': form})

from django.shortcuts import get_object_or_404

@login_required
def edit_daily_report(request, pk):
    report = get_object_or_404(DailyReport, pk=pk)
    if request.method == 'POST':
        form = DailyReportForm(request.POST, request.FILES, instance=report)
        if form.is_valid():
            form.save()
            return redirect('daily_reports_index')
    else:
        form = DailyReportForm(instance=report)
    return render(request, 'daily_reports/edit_daily_report.html', {'form': form, 'report': report})