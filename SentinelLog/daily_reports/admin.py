from django.contrib import admin
from .models import DailyReport

@admin.register(DailyReport)
class DailyReportAdmin(admin.ModelAdmin):
    list_display = ('date', 'report_type', 'uploaded_by', 'uploaded_at', 'pdf_file', 'related_case')
    list_filter = ('report_type', 'date', 'uploaded_by')
    search_fields = ('notes',)