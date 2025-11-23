from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .models import Apoderado, Alumno
from gestion.models import Concepto, RegistroPago

@login_required
def mi_perfil(request):
    try:
        apoderado = request.user.apoderado
    except Apoderado.DoesNotExist:
        return render(request, 'error_page.html', {'message': 'No se encontró un apoderado asociado a este usuario.'})

    alumno = apoderado.alumnos.first()
    if not alumno:
        return render(request, 'error_page.html', {'message': 'No se encontró un alumno asociado a este apoderado.'})

    conceptos_pagados_ids = RegistroPago.objects.filter(
        apoderado=apoderado,
        alumno=alumno
    ).values_list('concepto__id', flat=True).distinct()

    conceptos = Concepto.objects.filter(id__in=conceptos_pagados_ids)

    conceptos_data = []
    for concepto in conceptos:
        total_pagado = RegistroPago.objects.filter(
            apoderado=apoderado,
            alumno=alumno,
            concepto=concepto
        ).aggregate(sum_monto=Sum('monto_pagado'))['sum_monto'] or 0

        monto_total_concepto = concepto.monto_total

        porcentaje_pagado = 0
        estado_pago = "Pendiente"

        if monto_total_concepto > 0:
            porcentaje_pagado = min(int((total_pagado / monto_total_concepto) * 100), 100)
            if porcentaje_pagado == 100:
                estado_pago = "Pagado"
            elif porcentaje_pagado > 0:
                estado_pago = "Parcialmente Pagado"
        else:
            estado_pago = "N/A"

        conceptos_data.append({
            'nombre': concepto.nombre,
            'get_estado_pago_display': estado_pago,
            'es_pago_en_cuotas': concepto.numero_cuotas > 1,
            'porcentaje_pagado': porcentaje_pagado,
        })

    historial_data = []
    historial_data.append({
        'fecha': apoderado.user.date_joined.strftime('%Y-%m-%d'),
        'descripcion': f'Perfil de apoderado creado para {apoderado.nombres} {apoderado.apellidos}.'
    })
    historial_data.append({
        'fecha': '', # Placeholder, replace with actual association date
        'descripcion': f'Alumno {alumno.nombres} {alumno.apellidos} asociado al apoderado.'
    })
    historial_data.append({
        'fecha': '', # Placeholder
        'descripcion': f'Curso: {alumno.curso}, Colegio: {alumno.colegio}.'
    })

    registro_pagos = RegistroPago.objects.filter(
        apoderado=apoderado,
        alumno=alumno
    ).order_by('fecha')

    for rp in registro_pagos:
        historial_data.append({
            'fecha': rp.fecha.strftime('%Y-%m-%d'),
            'descripcion': f'Registro de pago: {rp.monto_pagado} para {rp.concepto.nombre} por {rp.metodo_pago}.'
        })
    
    # This sorting is not ideal with empty dates. A better approach would be to have creation dates on all models.
    # historial_data = sorted(historial_data, key=lambda x: x['fecha']) 

    context = {
        'perfil': {
            'alumno': {
                'nombre': alumno.nombres,
                'apellido': alumno.apellidos,
                'curso': {'nombre': alumno.curso},
                'colegio': {'nombre': alumno.colegio},
            },
            'fecha_creacion': apoderado.user.date_joined.strftime('%Y-%m-%d'),
            'fecha_asociacion_alumno': '', # Placeholder
            'conceptos': conceptos_data,
        },
        'historial': historial_data,
    }
    return render(request, 'perfiles/mi_perfil.html', context)
