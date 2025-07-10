from django.db import models
from django.contrib.auth import get_user_model
from simple_history.models import HistoricalRecords


class LostFoundItem(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendiente de procesar'),
        ('tramit', 'En tramite'),
        ('waiting', 'Esperando respuesta del propietario'),
        ('returned', 'Devuelto al propietario'),
        ('discarded', 'Descartado'),
        ('returned_to_associate', 'Entregado al asociado que encontró el objeto'),
        ('returned_to_other', 'Entregado a persona distinta del hallador o propietario'),
        ('dissapeared', 'Desaparecido/Perdido'),
    ]
    description = models.CharField(max_length=255)
    found_at = models.CharField(max_length=255)
    found_on = models.DateTimeField()
    found_by = models.CharField(max_length=255, default="Desconocido")
    photo = models.ImageField(upload_to='lostfound/photos/', blank=True, null=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='pending')
    returned_to = models.CharField(max_length=255, blank=True)
    returned_on = models.DateTimeField(blank=True, null=True)
    notes = models.TextField(blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.description} ({self.get_status_display()})"

class LostFoundNote(models.Model):
    item = models.ForeignKey(LostFoundItem, on_delete=models.CASCADE, related_name='notes_list')
    note = models.TextField()
    created_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Nota de {self.created_by} el {self.created_at:%d/%m/%Y %H:%M}"
    