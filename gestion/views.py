from django.http import JsonResponse
from perfiles.models import Apoderado, Alumno
from django.shortcuts import render

def get_alumnos_for_apoderado(request):
    apoderado_id = request.GET.get('apoderado_id')
    if apoderado_id:
        try:
            apoderado = Apoderado.objects.get(pk=apoderado_id)
            alumnos = apoderado.alumnos.all().values('alumno_id', 'nombres', 'apellidos')
            return JsonResponse({'alumnos': list(alumnos)})
        except Apoderado.DoesNotExist:
            return JsonResponse({'alumnos': []})
    return JsonResponse({'alumnos': []})
