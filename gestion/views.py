from django.http import JsonResponse
from perfiles.models import Alumno

def get_alumnos_for_apoderado(request):
    apoderado_id = request.GET.get('apoderado_id')
    alumnos = Alumno.objects.filter(apoderado_id=apoderado_id).order_by('nombres')
    return JsonResponse({'alumnos': list(alumnos.values('alumno_id', 'nombres', 'apellidos'))})