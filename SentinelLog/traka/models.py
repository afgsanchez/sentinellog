from django.db import models

class TrakaKeyUser(models.Model):
    DEPARTAMENTO_CHOICES = [
        ("Accounting", "Accounting"),
        ("Activities", "Activities"),
        ("Dirección", "Dirección"),
        ("Emergency", "Emergency"),
        ("Engineering", "Engineering"),
        ("Eulen", "Eulen"),
        ("F&B", "F&B"),
        ("Front Office", "Front Office"),
        ("Golf", "Golf"),
        ("Grounds", "Grounds"),
        ("Human Resources", "Human Resources"),
        ("Housekeeping", "Housekeeping"),
        ("IT", "IT"),
        ("MOD", "MOD"),
        ("Safety & Security", "Safety & Security"),
        ("Sales & Marketing", "Sales & Marketing"),
    ]
    SISTEMA_CHOICES = [
        ("PMI Tunnel", "PMI Tunnel"),
        ("pmimckeytra2 GARITA", "pmimckeytra2 GARITA"),
        ("pmimckeytra3 GROUND", "pmimckeytra3 GROUND"),
    ]
    TIPO_LLAVE_CHOICES = [
        ("Común", "Común"),
        ("Individual", "Individual"),
    ]

    nombre = models.CharField("Nombre", max_length=100)
    cargo = models.CharField("Cargo o posición", max_length=100)
    departamento = models.CharField("Departamento", max_length=30, choices=DEPARTAMENTO_CHOICES)
    sistema = models.CharField("Sistema", max_length=30, choices=SISTEMA_CHOICES)
    tipo_llave = models.CharField("Tipo de llave", max_length=15, choices=TIPO_LLAVE_CHOICES)
    posicion = models.PositiveIntegerField("Posición de la llave")
    acceso_anterior = models.TextField("Acceso anterior", blank=True)
    solicitud_pdf = models.FileField("Solicitud firmada (PDF)", upload_to="traka/solicitudes/", blank=True, null=True)
    fecha_asignacion = models.DateField("Fecha de asignación", auto_now_add=True)
    activo = models.BooleanField("Ocupada", default=True)  # True=ocupada, False=libre
    fecha_desasignacion = models.DateField("Fecha de desasignación", blank=True, null=True)


    class Meta:
        unique_together = ("sistema", "posicion")
        ordering = ["sistema", "posicion"]

    def __str__(self):
        return f"{self.nombre} - {self.sistema} #{self.posicion}"

    def esta_libre(self):
        return not self.activo
    
class TrakaKeyUserHistory(models.Model):
    sistema = models.CharField(max_length=30)
    posicion = models.PositiveIntegerField()
    nombre_anterior = models.CharField(max_length=100)
    nombre_nuevo = models.CharField(max_length=100)
    fecha_cambio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sistema} #{self.posicion}: {self.nombre_anterior} → {self.nombre_nuevo} ({self.fecha_cambio.date()})"
