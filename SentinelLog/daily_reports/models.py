from django.db import models
from django.contrib.auth.models import User

class DailyReport(models.Model):
    REPORT_TYPE_CHOICES = [
        ('vigilante', 'Vigilante de Seguridad'),
        ('front_gate', 'Control de Front Gate'),
        ('otro', 'Otro'),
    ]

    report_type = models.CharField(
        max_length=20,
        choices=REPORT_TYPE_CHOICES,
        default='vigilante'
    )
    date = models.DateField(help_text="Fecha a la que corresponde el informe")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    pdf_file = models.FileField(upload_to='daily_reports/pdfs/')
    related_case = models.ForeignKey(
        'investigations.InvestigationCase',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Relaciona este informe con un caso de investigación si aplica"
    )
    notes = models.TextField(blank=True, help_text="Notas u observaciones adicionales")
    pdf_text = models.TextField(blank=True, help_text="Texto extraído del PDF para búsqueda")

    def __str__(self):
        return f"{self.get_report_type_display()} - {self.date} ({self.pdf_file.name.split('/')[-1]})"