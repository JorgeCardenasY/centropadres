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

    # Obtener todos los conceptos (no solo los que tienen pagos)
    conceptos = Concepto.objects.all()

    conceptos_data = []
    for concepto in conceptos:
        total_pagado = RegistroPago.objects.filter(
            apoderado=apoderado,
            alumno=alumno,
            concepto=concepto
        ).aggregate(sum_monto=Sum('monto_pagado'))['sum_monto'] or 0

        monto_total_concepto = concepto.monto_total
        monto_pendiente = max(monto_total_concepto - total_pagado, 0)

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
            'numero_cuotas': concepto.numero_cuotas,
            'monto_total': monto_total_concepto,
            'monto_pagado': total_pagado,
            'monto_pendiente': monto_pendiente,
            'estado_pago': estado_pago,
            'es_pago_en_cuotas': concepto.numero_cuotas > 1,
            'porcentaje_pagado': porcentaje_pagado,
        })

    # Obtener apoderados con flag de reportador (tesoreros)
    # Asumiendo que el campo se llama 'registrar_pago' o necesitamos crear uno nuevo
    tesoreros = Apoderado.objects.filter(registrar_pago=True)
    
    # Preparar información de tesoreros para el mensaje
    info_tesoreros = []
    for tesorero in tesoreros:
        info_tesoreros.append({
            'nombre': f"{tesorero.nombres} {tesorero.apellidos}",
            'telefono': tesorero.telefono
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

    context = {
        'perfil': {
            'alumno': {
                'nombre': alumno.nombres,
                'apellido': alumno.apellidos,
                'curso': alumno.curso,
                'colegio': alumno.colegio,
            },
            'fecha_creacion': apoderado.user.date_joined.strftime('%Y-%m-%d'),
            'fecha_asociacion_alumno': '', # Placeholder
            'conceptos': conceptos_data,
        },
        'historial': historial_data,
        'tesoreros': info_tesoreros,
    }
    return render(request, 'perfiles/mi_perfil.html', context)
