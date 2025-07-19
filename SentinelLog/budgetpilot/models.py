from django.db import models
from simple_history.models import HistoricalRecords

class Proveedor(models.Model):
    nombre = models.CharField(max_length=255)
    categoria = models.ForeignKey('CategoriaProveedor', on_delete=models.SET_NULL, null=True, blank=True)
    cif = models.CharField("CIF/NIF", max_length=20, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    persona_contacto = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.nombre


class Presupuesto(models.Model):
    ESTADOS = [
        ('pendiente_aprobacion', 'Pendiente de aprobación'),
        ('aprobado', 'Aprobado'),
        ('en_ejecucion', 'En ejecución'),
        ('completado', 'Completado'),
        ('rechazado', 'Rechazado'),
    ]

    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    numero = models.CharField("Número de presupuesto", max_length=100)
    fecha = models.DateField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    documento = models.FileField(upload_to='presupuestos/')
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente_aprobacion')
    fecha_entrega_estimada = models.DateField(blank=True, null=True)
    responsable = models.CharField(max_length=255, blank=True, null=True)
    comentarios = models.TextField(blank=True, null=True)

    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    history = HistoricalRecords()

    def __str__(self):
        return f"{self.numero} - {self.proveedor.nombre}"

class CategoriaProveedor(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre


class NotificacionInterna(models.Model):
    mensaje = models.TextField()
    presupuesto = models.ForeignKey(Presupuesto, on_delete=models.CASCADE, related_name='notificaciones')
    leido = models.BooleanField(default=False)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notificación para {self.presupuesto.numero}"

class AdjuntoPresupuesto(models.Model):
    presupuesto = models.ForeignKey(Presupuesto, on_delete=models.CASCADE, related_name='adjuntos')
    archivo = models.FileField(upload_to='presupuestos/adjuntos/')
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    fecha_subida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Adjunto para {self.presupuesto.numero}"

class HistorialEstadoPresupuesto(models.Model):
    presupuesto = models.ForeignKey(Presupuesto, on_delete=models.CASCADE, related_name='historial_estados')
    estado = models.CharField(max_length=20, choices=Presupuesto.ESTADOS)
    fecha = models.DateTimeField(auto_now_add=True)
    comentario = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.presupuesto.numero} → {self.get_estado_display()} en {self.fecha.strftime('%Y-%m-%d')}"
