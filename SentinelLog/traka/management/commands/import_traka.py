from django.core.management.base import BaseCommand
from traka.models import TrakaKeyUser, TrakaKeyUserHistory
import pandas as pd
from datetime import date

class Command(BaseCommand):
    help = "Importa datos de llaves Traka desde un archivo Excel"

    def add_arguments(self, parser):
        parser.add_argument("excel_file", type=str, help="Ruta al archivo Excel (.xlsx)")

    def handle(self, *args, **kwargs):
        excel_file = kwargs["excel_file"]

        departamento_map = {
            "DIRECCION": "Dirección",
            "ENG": "Engineering",
            "HSKP": "Housekeeping",
            "IT": "IT",
            "GROUNDS": "Grounds",
            "F&B": "F&B",
            "F&amp;B": "F&B",
            "SAFETY & SECURITY": "Safety & Security",
            "Seguridad": "Safety & Security",
        }

        sistema_map = {
            "PMI Tunnel": "PMI Tunnel",
            "pmimckeytra2 GARITA": "pmimckeytra2 GARITA",
            "pmimckeytra3 GROUND": "pmimckeytra3 GROUND",
        }

        tipo_llave_map = {
            "I": "Individual",
            "C": "Común",
            "": "Común",
        }

        try:
            df = pd.read_excel(excel_file, engine="openpyxl")
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error al leer el archivo: {e}"))
            return

        total = 0
        for _, row in df.iterrows():
            nombre = str(row.get("Quién", "")).strip()
            cargo = str(row.get("Puesto", "")).strip()
            departamento = departamento_map.get(str(row.get("Departamento", "")).strip(), str(row.get("Departamento", "")).strip())
            sistema = sistema_map.get(str(row.get("Sistema", "")).strip(), str(row.get("Sistema", "")).strip())
            tipo_llave = tipo_llave_map.get(str(row.get("Comun/Individual", "")).strip(), "Común")
            posicion = row.get("Pos.")
            acceso_anterior = str(row.get("Acceso Anterior", "")).strip()

            if pd.isna(posicion):
                continue

            try:
                posicion = int(posicion)
            except ValueError:
                continue

            # Si el nombre está vacío o es 'nan', marcar como libre
            if not nombre or nombre.lower() == "nan":
                TrakaKeyUser.objects.update_or_create(
                    sistema=sistema,
                    posicion=posicion,
                    defaults={
                        "nombre": "",
                        "cargo": cargo,
                        "departamento": departamento,
                        "tipo_llave": tipo_llave,
                        "acceso_anterior": acceso_anterior,
                        "activo": False,
                        "fecha_desasignacion": None,
                    }
                )
                total += 1
                self.stdout.write(f"Libre: {sistema} #{posicion}")
                continue

            try:
                existente = TrakaKeyUser.objects.get(sistema=sistema, posicion=posicion)
                if existente.nombre != nombre:
                    TrakaKeyUserHistory.objects.create(
                        sistema=sistema,
                        posicion=posicion,
                        nombre_anterior=existente.nombre,
                        nombre_nuevo=nombre
                    )
                    existente.fecha_desasignacion = date.today()
                    existente.save()

                    if acceso_anterior:
                        acceso_anterior = f"{existente.nombre}, {acceso_anterior}"
                    else:
                        acceso_anterior = existente.nombre
            except TrakaKeyUser.DoesNotExist:
                pass

            TrakaKeyUser.objects.update_or_create(
                sistema=sistema,
                posicion=posicion,
                defaults={
                    "nombre": nombre,
                    "cargo": cargo,
                    "departamento": departamento,
                    "tipo_llave": tipo_llave,
                    "acceso_anterior": acceso_anterior,
                    "activo": True,
                    "fecha_desasignacion": None,
                }
            )
            total += 1
            self.stdout.write(f"Asignado: {nombre} - {sistema} #{posicion}")

        self.stdout.write(self.style.SUCCESS(f"Importación completada. Total de registros procesados: {total}"))
