from django.db import models

class RegistroAcceso(models.Model):
    TIPO_CHOICES = [
        ('entrada_salida', 'Entradas y Salidas'),
        ('visita', 'Visitas'),
    ]
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    fecha = models.DateField()
    # hora_entrada = models.TimeField(null=True, blank=True)
    hora_entrada = models.CharField(max_length=10, blank=True)
    matricula = models.CharField(max_length=30, blank=True)
    nombre_apellidos = models.CharField(max_length=100)
    nombre_empresa = models.CharField(max_length=100, blank=True)
    donde_se_dirigen = models.CharField(max_length=100, blank=True)
    # hora_salida = models.TimeField(blank=True, null=True)
    hora_salida = models.CharField(max_length=10, blank=True)
    entrega_tarjeta = models.CharField(max_length=30, blank=True)
    devolucion_tarjeta = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return f"{self.fecha} - {self.nombre_apellidos} ({self.tipo})"