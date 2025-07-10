from simple_history.models import HistoricalRecords
from django.db import models

class GrupoTraka(models.Model):
    tipo_tarjeta = models.CharField(max_length=100)
    localizacion_tarjeta = models.CharField(max_length=100, blank=True)
    fecha_caducidad = models.DateField()

    def __str__(self):
        return f"{self.tipo_tarjeta} ({self.localizacion_tarjeta})"

