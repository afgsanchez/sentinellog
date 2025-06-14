from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='investigations_index'),
    path('case/add/', views.add_case, name='add_case'),
    path('case/<int:case_id>/', views.case_detail, name='case_detail'),
    path('case/<int:case_id>/document/add/', views.add_document, name='add_document'),
    path('case/<int:case_id>/comment/add/', views.add_comment, name='add_comment'),
    path('case/<int:case_id>/interview/add/', views.add_interview, name='add_interview'),
    path('case/<int:case_id>/report/pdf/', views.generate_pdf_report, name='generate_pdf_report'),
    path('cases/<int:case_id>/save_pdf/', views.save_pdf_report, name='save_pdf_report'),
]
