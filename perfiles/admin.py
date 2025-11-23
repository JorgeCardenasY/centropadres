from django.contrib.auth.models import User
from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Apoderado, Alumno
from centropadres.admin import my_admin_site
import csv
from django.db import transaction


class AlumnoAdmin(admin.ModelAdmin):
    list_display = ('nombres', 'apellidos', 'rut_dni', 'curso', 'colegio', 'apoderado')
    search_fields = ('nombres', 'apellidos', 'rut_dni')
    list_filter = ('colegio', 'curso')

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('upload-csv/', self.admin_site.admin_view(self.upload_csv), name='perfiles_alumno_upload_csv'),
        ]
        return my_urls + urls

    def upload_csv(self, request):
        if request.method == 'POST':
            csv_file = request.FILES.get('csv_file')
            if not csv_file or not csv_file.name.endswith('.csv'):
                self.message_user(request, "Por favor, suba un archivo CSV válido.", level=messages.ERROR)
                return redirect('.')

            successful_uploads = []
            failed_uploads = []
            
            try:
                decoded_file = csv_file.read().decode('utf-8').splitlines()
                reader = csv.DictReader(decoded_file)
                
                headers = ['apoderado_nombres', 'apoderado_apellidos', 'apoderado_rut_dni', 
                           'apoderado_telefono', 'apoderado_direccion', 'apoderado_whatsapp', 
                           'alumno_nombres', 'alumno_apellidos', 'alumno_rut_dni', 
                           'alumno_curso', 'alumno_colegio']

                if not all(header in reader.fieldnames for header in headers):
                    self.message_user(request, f'El encabezado del CSV es incorrecto. Debe contener: {", ".join(headers)}', level=messages.ERROR)
                    return redirect('.')


                for i, row in enumerate(reader):
                    row_number = i + 2
                    try:
                        with transaction.atomic():
                            apoderado_rut = row.get('apoderado_rut_dni')
                            if not apoderado_rut:
                                raise ValueError("El RUT/DNI del apoderado es obligatorio.")
                            
                            apoderado, created = Apoderado.objects.get_or_create(
                                rut_dni=apoderado_rut,
                                defaults={
                                    'nombres': row.get('apoderado_nombres'),
                                    'apellidos': row.get('apoderado_apellidos'),
                                    'telefono': row.get('apoderado_telefono'),
                                    'direccion': row.get('apoderado_direccion'),
                                    'whatsapp': row.get('apoderado_whatsapp')
                                }
                            )

                            alumno_rut = row.get('alumno_rut_dni')
                            if not alumno_rut:
                                 raise ValueError("El RUT/DNI del alumno es obligatorio.")

                            if Alumno.objects.filter(rut_dni=alumno_rut).exists():
                                raise ValueError(f"El alumno con RUT/DNI {alumno_rut} ya existe.")

                            alumno = Alumno.objects.create(
                                nombres=row.get('alumno_nombres'),
                                apellidos=row.get('alumno_apellidos'),
                                rut_dni=alumno_rut,
                                curso=row.get('alumno_curso'),
                                colegio=row.get('alumno_colegio'),
                                apoderado=apoderado
                            )
                            successful_uploads.append(alumno)

                    except ValueError as ve:
                        failed_uploads.append({'row_number': row_number, 'error': str(ve), 'data': row})
                    except Exception as e:
                        failed_uploads.append({'row_number': row_number, 'error': f'Error inesperado: {str(e)}', 'data': row})

            except Exception as e:
                self.message_user(request, f'Error al procesar el archivo: {str(e)}', level=messages.ERROR)
                return redirect('.')
            
            context = {
                'successful_uploads': successful_uploads,
                'failed_uploads': failed_uploads,
                'success_count': len(successful_uploads),
                'error_count': len(failed_uploads),
                'opts': self.model._meta,
                'has_change_permission': self.has_change_permission(request)
            }
            
            if failed_uploads:
                self.message_user(request, "Algunos registros no se pudieron cargar.", level=messages.WARNING)
            if successful_uploads:
                self.message_user(request, f"{len(successful_uploads)} alumnos cargados correctamente.", level=messages.SUCCESS)

            return render(request, 'admin/perfiles/alumno/upload_results.html', context)


        context = {
            'opts': self.model._meta,
            'has_change_permission': self.has_change_permission(request)
        }
        return render(request, 'admin/perfiles/alumno/upload_csv.html', context)

class ApoderadoAdmin(admin.ModelAdmin):
    list_display = ('nombres', 'apellidos', 'rut_dni', 'telefono', 'registrar_pago')
    search_fields = ('nombres', 'apellidos', 'rut_dni')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            kwargs["queryset"] = User.objects.filter(is_staff=False, is_superuser=False)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

my_admin_site.register(Alumno, AlumnoAdmin)
my_admin_site.register(Apoderado, ApoderadoAdmin)
