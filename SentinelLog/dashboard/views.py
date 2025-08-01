from django.shortcuts import render
from daily_reports.models import DailyReport
from incident_management.models import Incident
from investigations.models import InvestigationCase
from lostfound.models import LostFoundItem
from traka.models import TrakaKeyUserHistory
from visionline.models import VisionlineOperator
from .models import GrupoTraka
from datetime import date, timedelta
from django.http import JsonResponse
from utils.code_generator import generar_codigo_unico


def dashboard_view(request):
    context = {
        # Últimos 3 movimientos por modelo
        'ultimos_daily_reports': DailyReport.history.all().order_by('-history_date')[:3],
        'ultimos_incidentes': Incident.history.all().order_by('-history_date')[:3],
        'ultimas_investigaciones': InvestigationCase.history.all().order_by('-history_date')[:3],
        'ultimos_objetos_perdidos': LostFoundItem.history.all().order_by('-history_date')[:3],
        'ultimos_traka': TrakaKeyUserHistory.history.all().order_by('-history_date')[:3],
        'ultimos_visionline': VisionlineOperator.history.all().order_by('-history_date')[:3],

        # Totales por modelo
        'total_daily_reports': DailyReport.history.count(),
        'total_incidentes': Incident.history.count(),
        'total_investigaciones': InvestigationCase.history.count(),
        'total_objetos_perdidos': LostFoundItem.history.count(),
        'total_traka': TrakaKeyUserHistory.history.count(),
        'total_visionline': VisionlineOperator.history.count(),
    }

    ...
    context['grupos_traka'] = GrupoTraka.objects.all()
    context['today'] = date.today()
    context['today_plus_2'] = date.today() + timedelta(days=2)

    return render(request, 'dashboard/dashboard.html', context)

def index(request):
    return render(request, 'dashboard/index.html')



def generar_codigo_view(request):
    if request.method == 'GET':
        codigo = generar_codigo_unico()
        return JsonResponse({'codigo': codigo})
