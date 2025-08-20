from django.core.management.base import BaseCommand
from registros_accesos.models import RegistroAcceso
import pandas as pd

class Command(BaseCommand):
    help = 'Importa registros desde el archivo Excel'

    def handle(self, *args, **kwargs):
        file_path = 'datatraka.xlsx'
        hojas = {
            'ENTRADAS Y SALIDAS': 'entrada_salida',
            'VISITAS': 'visita'
        }
        for hoja, tipo in hojas.items():
            df = pd.read_excel(file_path, sheet_name=hoja)
            for _, row in df.iterrows():
                RegistroAcceso.objects.create(
                    tipo=tipo,
                    fecha=row['FECHA'],
                    hora_entrada=row['HORA ENTRADA'],
                    matricula=row.get('MATRÍCULA', ''),
                    nombre_apellidos=row['NOMBRE Y APELLIDOS'],
                    nombre_empresa=row.get('NOMBRE EMPRESA', ''),
                    donde_se_dirigen=row.get('DONDE SE DIRIGEN', ''),
                    hora_salida=row.get('HORA SALIDA'),
                    entrega_tarjeta=row.get('ENTREGA TARJETA', ''),
                    devolucion_tarjeta=row.get('DEVOLUCIÓN TARJETA', ''),
                )
        self.stdout.write(self.style.SUCCESS('Registros importados correctamente'))