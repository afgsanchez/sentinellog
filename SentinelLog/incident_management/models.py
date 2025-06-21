from django.db import models
from django.contrib.auth.models import User

class IncidentType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Incident(models.Model):
    # INCIDENT_TYPE_CHOICES = [
    #     ('robo', 'Robo'),
    #     ('caida', 'Caída'),
    #     ('colision', 'Colisión de Vehículo'),
    #     ('golpe', 'Golpe'),
    #     ('desmayo', 'Desmayo'),
    #     ('otro', 'Otro'),
    # ]
    incident_type = models.ForeignKey(IncidentType, on_delete=models.PROTECT, null=True)
    affected_person = models.CharField("Persona afectada", max_length=100, blank=True, null=True)
    date = models.DateTimeField(help_text="Fecha y hora del incidente")
    location = models.CharField(max_length=255)
    description = models.TextField()
    reported_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='incidents_reported')
    # incident_report_pdf = models.FileField(upload_to='incident_reports/pdfs/')
    incident_report_docx = models.FileField(upload_to='incident_reports/docx/', null=True, blank=True, help_text="Archivo DOCX del Incident Report")
    insurance_case_number = models.CharField(max_length=100, blank=True, help_text="Número de caso de la aseguradora")
    related_investigation = models.ForeignKey(
        'investigations.InvestigationCase',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Relaciona este incidente con una investigación si aplica"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    docx_text = models.TextField(blank=True, help_text="Texto extraído del DOCX para búsqueda")

    def __str__(self):
        tipo = self.incident_type.name if self.incident_type else "Sin tipo"
        return f"{tipo} - {self.date.strftime('%d/%m/%Y %H:%M')}"

class IncidentPhoto(models.Model):
    incident = models.ForeignKey(Incident, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='incident_reports/photos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

class IncidentNote(models.Model):
    incident = models.ForeignKey(Incident, on_delete=models.CASCADE, related_name='notes')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    note = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class IncidentAttachment(models.Model):
    incident = models.ForeignKey(Incident, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='incident_reports/attachments/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.file.name.split('/')[-1]