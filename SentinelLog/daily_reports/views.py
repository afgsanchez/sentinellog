from django.shortcuts import render

def index(request):
    return render(request, 'daily_reports/index.html')
