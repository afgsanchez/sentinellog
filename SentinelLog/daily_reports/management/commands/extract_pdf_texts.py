from django.core.management.base import BaseCommand
from daily_reports.models import DailyReport
import PyPDF2

class Command(BaseCommand):
    help = 'Extrae el texto de los PDFs ya subidos y lo guarda en el campo pdf_text'

    def handle(self, *args, **kwargs):
        updated = 0
        for report in DailyReport.objects.all():
            if report.pdf_file and (not report.pdf_text or report.pdf_text.strip() == ""):
                try:
                    with report.pdf_file.open('rb') as f:
                        reader = PyPDF2.PdfReader(f)
                        text = ""
                        for page in reader.pages:
                            text += page.extract_text() or ""
                        report.pdf_text = text
                        report.save()
                        updated += 1
                        self.stdout.write(self.style.SUCCESS(f"Actualizado informe {report.pk}"))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error en informe {report.pk}: {e}"))
        self.stdout.write(self.style.SUCCESS(f"¡Listo! {updated} informes actualizados."))