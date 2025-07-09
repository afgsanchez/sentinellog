from django.core.management.base import BaseCommand
from traka.models import TrakaKeyUserHistory
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from django.utils.timezone import localtime

class Command(BaseCommand):
    help = "Exporta el historial de cambios de llaves Traka a un archivo PDF"

    def handle(self, *args, **kwargs):
        filename = "traka_historial.pdf"
        c = canvas.Canvas(filename, pagesize=A4)
        width, height = A4

        c.setFont("Helvetica-Bold", 14)
        c.drawString(2 * cm, height - 2 * cm, "Historial de cambios de llaves Traka")

        c.setFont("Helvetica", 10)
        y = height - 3 * cm
        line_height = 0.6 * cm

        headers = ["Sistema", "Posición", "Nombre anterior", "Nombre nuevo", "Fecha de cambio"]
        for i, header in enumerate(headers):
            c.drawString((2 + i * 4) * cm, y, header)

        y -= line_height

        historial = TrakaKeyUserHistory.objects.all().order_by("-fecha_cambio")

        for cambio in historial:
            if y < 2 * cm:
                c.showPage()
                y = height - 2 * cm
                c.setFont("Helvetica", 10)

            c.drawString(2 * cm, y, cambio.sistema)
            c.drawString(6 * cm, y, str(cambio.posicion))
            c.drawString(10 * cm, y, cambio.nombre_anterior[:20])
            c.drawString(14 * cm, y, cambio.nombre_nuevo[:20])
            c.drawString(18 * cm, y, localtime(cambio.fecha_cambio).strftime("%Y-%m-%d %H:%M"))
            y -= line_height

        c.save()
        self.stdout.write(self.style.SUCCESS(f"PDF generado correctamente: {filename}"))
