from django.db import models
from simple_history.models import HistoricalRecords


class VisionlineOperator(models.Model):
    # Sección 1
    request_date = models.DateField("Fecha de solicitud")
    full_name = models.CharField("Nombre y apellidos", max_length=100)
    position = models.CharField("Cargo o posición", max_length=100)
    eid = models.CharField("EID", max_length=50)
    department = models.CharField("Departamento", max_length=100)

    # Sección 2
    ACCESS_CHOICES = [
        ("activities", "Activities"),
        ("basico", "Básico"),
        ("golf", "Golf"),
        ("supervisor_engineering", "Supervisor Engineering"),
        ("system_manager", "System Manager"),
    ]
    access_required = models.CharField("Acceso requerido", max_length=30, choices=ACCESS_CHOICES)

    # Sección 3
    setup_by = models.CharField("Setup by", max_length=100)
    completion_date = models.DateField("Date of completion")
    username_assigned = models.CharField("Username assigned", max_length=100)
    password_assigned = models.CharField("Password assigned (base64)", max_length=255)
    is_active = models.BooleanField("Activo", default=True)

    # Sección 4
    manager_signed = models.CharField("Manager que firma la solicitud", max_length=100)

    # Documento adjunto
    request_pdf = models.FileField("Solicitud firmada (PDF)", upload_to="visionline/requests/")

    created_at = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.full_name} ({self.username_assigned})"