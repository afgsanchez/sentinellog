from django.shortcuts import render, redirect
from .models import RegistroAcceso
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
import pandas as pd
from io import BytesIO
from datetime import datetime, time



def registro_list(request):
    qs = RegistroAcceso.objects.all().order_by('-fecha', '-hora_entrada')

    # Búsqueda general
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(
            Q(fecha__icontains=search) |
            Q(hora_entrada__icontains=search) |
            Q(matricula__icontains=search) |
            Q(nombre_apellidos__icontains=search) |
            Q(nombre_empresa__icontains=search) |
            Q(donde_se_dirigen__icontains=search) |
            Q(hora_salida__icontains=search) |
            Q(entrega_tarjeta__icontains=search) |
            Q(devolucion_tarjeta__icontains=search)
        )

    # Filtro por rango de fechas
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    if date_from:
        qs = qs.filter(fecha__gte=date_from)
    if date_to:
        qs = qs.filter(fecha__lte=date_to)

    # Ordenación
    ordering = request.GET.get('ordering', '-fecha')
    if ordering:
        qs = qs.order_by(ordering, '-hora_entrada')

    # Paginación
    paginator = Paginator(qs, 25)  # 25 por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search': search,
        'date_from': date_from,
        'date_to': date_to,
        'ordering': ordering,
    }
    return render(request, 'registros_accesos/registro_list.html', context)





def registro_import(request):
    if request.method == "POST" and request.FILES.get("excel_file"):
        excel_file = request.FILES["excel_file"]
        hojas = {
            'ENTRADAS Y SALIDAS': 'entrada_salida',
            'VISITAS': 'visita'
        }
        try:
            in_memory_file = BytesIO(excel_file.read())
            xls = pd.ExcelFile(in_memory_file)
            total_importados = 0
            total_omitidos = 0

            for hoja, tipo in hojas.items():
                if hoja in xls.sheet_names:
                    df = pd.read_excel(xls, sheet_name=hoja)
                    df = df.dropna(how='all')

                    for _, row in df.iterrows():
                        fecha_raw = row.get('FECHA')
                        campos_extra = [
                            row.get('HORA ENTRADA'),
                            row.get('MATRÍCULA'),
                            row.get('NOMBRE Y APELLIDOS'),
                            row.get('NOMBRE EMPRESA'),
                            row.get('DONDE SE DIRIGEN'),
                            row.get('HORA SALIDA'),
                            row.get('ENTREGA TARJETA'),
                            row.get('DEVOLUCIÓN TARJETA'),
                        ]

                        if pd.notna(fecha_raw) and any(pd.notna(campo) and str(campo).strip() != "" for campo in campos_extra):
                            try:
                                fecha = pd.to_datetime(fecha_raw, errors='coerce')
                                if pd.isna(fecha):
                                    fecha = datetime.today().date()

                                RegistroAcceso.objects.create(
                                    tipo=tipo,
                                    fecha=fecha,
                                    hora_entrada=str(row.get('HORA ENTRADA')) if pd.notna(row.get('HORA ENTRADA')) else "",
                                    matricula=row.get('MATRÍCULA', ''),
                                    nombre_apellidos=row.get('NOMBRE Y APELLIDOS', '') or "Desconocido",
                                    nombre_empresa=row.get('NOMBRE EMPRESA', ''),
                                    donde_se_dirigen=row.get('DONDE SE DIRIGEN', ''),
                                    hora_salida=str(row.get('HORA SALIDA')) if pd.notna(row.get('HORA SALIDA')) else "",
                                    entrega_tarjeta=row.get('ENTREGA TARJETA', ''),
                                    devolucion_tarjeta=row.get('DEVOLUCIÓN TARJETA', ''),
                                )
                                total_importados += 1
                            except Exception as e:
                                print(f"Error al crear registro: {e}")
                                total_omitidos += 1
                        else:
                            total_omitidos += 1

            messages.success(request, f"Importación completada. {total_importados} registros importados, {total_omitidos} omitidos.")
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            messages.error(request, f"Error al importar: {e}")
    return redirect('registro_list')
