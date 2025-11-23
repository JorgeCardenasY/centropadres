from django.contrib.auth.models import User, Permission
from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.contenttypes.models import ContentType
from .models import Apoderado, Alumno
from gestion.models import Concepto, RegistroPago
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
                # Try decoding with UTF-8, then fallback to latin-1
                file_content = csv_file.read()
                try:
                    decoded_file = file_content.decode('utf-8').splitlines()
                except UnicodeDecodeError:
                    decoded_file = file_content.decode('latin-1').splitlines()

                reader = csv.DictReader(decoded_file)
                
                headers = ['apoderado_nombres', 'apoderado_apellidos', 'apoderado_rut_dni', 
                           'apoderado_telefono', 'apoderado_direccion', 'apoderado_whatsapp', 
                           'alumno_nombres', 'alumno_apellidos', 'alumno_rut_dni', 
                           'alumno_curso', 'alumno_colegio']

                if not all(header in reader.fieldnames for header in headers):
                    self.message_user(request, f'El encabezado del CSV es incorrecto. Debe contener: {", ".join(headers)}', level=messages.ERROR)
                    return redirect('.')


                usuarios_creados = 0
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

                            # Crear usuario automáticamente si el apoderado es nuevo y no tiene usuario
                            if created and not apoderado.user:
                                try:
                                    # Crear nombre de usuario basado en el RUT (sin puntos ni guión)
                                    username = apoderado.rut_dni.replace('.', '').replace('-', '').lower()
                                    
                                    # Verificar si el username ya existe
                                    if User.objects.filter(username=username).exists():
                                        # Si existe, agregar sufijo numérico
                                        counter = 1
                                        while User.objects.filter(username=f"{username}{counter}").exists():
                                            counter += 1
                                        username = f"{username}{counter}"

                                    # Crear contraseña por defecto 'password123'
                                    password_default = 'password123'

                                    # Crear el usuario
                                    user = User.objects.create(
                                        username=username,
                                        password=make_password(password_default),
                                        first_name=apoderado.nombres,
                                        last_name=apoderado.apellidos,
                                        email=f"{username}@centropadres.cl",
                                        is_active=True,
                                        is_staff=False,
                                        is_superuser=False
                                    )

                                    # Asignar permisos por defecto al usuario Apoderado
                                    self._asignar_permisos_por_defecto(user)

                                    # Asociar el usuario al apoderado
                                    apoderado.user = user
                                    apoderado.save()

                                    usuarios_creados += 1

                                except Exception as user_error:
                                    # Si hay error creando usuario, continuar con el proceso pero registrar el error
                                    failed_uploads.append({'row_number': row_number, 'error': f"Error creando usuario: {str(user_error)}", 'data': row})
                                    # Continuar con la creación del alumno aunque falle la creación del usuario

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
                'usuarios_creados': usuarios_creados,
                'opts': self.model._meta,
                'has_change_permission': self.has_change_permission(request)
            }
            
            if failed_uploads:
                self.message_user(request, "Algunos registros no se pudieron cargar.", level=messages.WARNING)
            if successful_uploads:
                self.message_user(request, f"{len(successful_uploads)} alumnos cargados correctamente.", level=messages.SUCCESS)
            if usuarios_creados > 0:
                self.message_user(request, f"{usuarios_creados} usuarios creados automáticamente con contraseña 'password123'.", level=messages.SUCCESS)

            return render(request, 'admin/perfiles/alumno/upload_results.html', context)


        context = {
            'opts': self.model._meta,
            'has_change_permission': self.has_change_permission(request)
        }
        return render(request, 'admin/perfiles/alumno/upload_csv.html', context)

    def _asignar_permisos_por_defecto(self, user):
        """Asigna los permisos por defecto a un usuario Apoderado"""
        try:
            # Obtener los ContentTypes para los modelos
            concepto_content_type = ContentType.objects.get_for_model(Concepto)
            registro_pago_content_type = ContentType.objects.get_for_model(RegistroPago)
            alumno_content_type = ContentType.objects.get_for_model(Alumno)

            # Obtener los permisos específicos
            permisos = [
                # Gestion | concepto | Can view concepto
                Permission.objects.get(
                    content_type=concepto_content_type,
                    codename='view_concepto'
                ),
                # Gestion | registro pago | Can view registro pago
                Permission.objects.get(
                    content_type=registro_pago_content_type,
                    codename='view_registropago'
                ),
                # Perfiles | alumno | Can view alumno
                Permission.objects.get(
                    content_type=alumno_content_type,
                    codename='view_alumno'
                ),
            ]

            # Asignar los permisos al usuario
            user.user_permissions.set(permisos)
            user.save()

        except Permission.DoesNotExist as e:
            raise Exception(f"Error al obtener permisos: {str(e)}")
        except Exception as e:
            raise Exception(f"Error al asignar permisos: {str(e)}")

class ApoderadoAdmin(admin.ModelAdmin):
    list_display = ('nombres', 'apellidos', 'rut_dni', 'telefono', 'registrar_pago', 'tiene_cuenta_usuario')
    search_fields = ('nombres', 'apellidos', 'rut_dni')
    actions = ['crear_cuentas_usuario']

    def tiene_cuenta_usuario(self, obj):
        return "Sí" if obj.user else "No"
    tiene_cuenta_usuario.short_description = 'Tiene Cuenta'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            kwargs["queryset"] = User.objects.filter(is_staff=False, is_superuser=False)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def crear_cuentas_usuario(self, request, queryset):
        """Acción para crear cuentas de usuario para apoderados seleccionados"""
        cuentas_creadas = 0
        cuentas_existentes = 0
        errores = []

        for apoderado in queryset:
            # Verificar si ya tiene una cuenta de usuario
            if apoderado.user:
                cuentas_existentes += 1
                continue

            try:
                # Crear nombre de usuario basado en el RUT (sin puntos ni guión)
                username = apoderado.rut_dni.replace('.', '').replace('-', '').lower()
                
                # Verificar si el username ya existe
                if User.objects.filter(username=username).exists():
                    # Si existe, agregar sufijo numérico
                    counter = 1
                    while User.objects.filter(username=f"{username}{counter}").exists():
                        counter += 1
                    username = f"{username}{counter}"

                # Crear contraseña temporal (primeros 6 caracteres del RUT)
                password_temp = apoderado.rut_dni.replace('.', '').replace('-', '')[:6]

                # Crear el usuario
                user = User.objects.create(
                    username=username,
                    password=make_password(password_temp),
                    first_name=apoderado.nombres,
                    last_name=apoderado.apellidos,
                    email=f"{username}@centropadres.cl",
                    is_active=True,
                    is_staff=False,
                    is_superuser=False
                )

                # Asignar permisos por defecto al usuario Apoderado
                self._asignar_permisos_por_defecto(user)

                # Asociar el usuario al apoderado
                apoderado.user = user
                apoderado.save()

                cuentas_creadas += 1

            except Exception as e:
                errores.append(f"Error creando cuenta para {apoderado.nombres} {apoderado.apellidos}: {str(e)}")

        # Mostrar mensajes de resultado
        if cuentas_creadas > 0:
            self.message_user(
                request, 
                f"Se crearon {cuentas_creadas} cuentas de usuario exitosamente con permisos por defecto.", 
                level=messages.SUCCESS
            )
        
        if cuentas_existentes > 0:
            self.message_user(
                request, 
                f"{cuentas_existentes} apoderados ya tenían cuentas de usuario.", 
                level=messages.WARNING
            )
        
        if errores:
            for error in errores:
                self.message_user(request, error, level=messages.ERROR)

    crear_cuentas_usuario.short_description = "Crear cuentas de usuario para apoderados seleccionados"

    def _asignar_permisos_por_defecto(self, user):
        """Asigna los permisos por defecto a un usuario Apoderado"""
        try:
            # Obtener los ContentTypes para los modelos
            concepto_content_type = ContentType.objects.get_for_model(Concepto)
            registro_pago_content_type = ContentType.objects.get_for_model(RegistroPago)
            alumno_content_type = ContentType.objects.get_for_model(Alumno)

            # Obtener los permisos específicos
            permisos = [
                # Gestion | concepto | Can view concepto
                Permission.objects.get(
                    content_type=concepto_content_type,
                    codename='view_concepto'
                ),
                # Gestion | registro pago | Can view registro pago
                Permission.objects.get(
                    content_type=registro_pago_content_type,
                    codename='view_registropago'
                ),
                # Perfiles | alumno | Can view alumno
                Permission.objects.get(
                    content_type=alumno_content_type,
                    codename='view_alumno'
                ),
            ]

            # Asignar los permisos al usuario
            user.user_permissions.set(permisos)
            user.save()

        except Permission.DoesNotExist as e:
            raise Exception(f"Error al obtener permisos: {str(e)}")
        except Exception as e:
            raise Exception(f"Error al asignar permisos: {str(e)}")

my_admin_site.register(Alumno, AlumnoAdmin)
my_admin_site.register(Apoderado, ApoderadoAdmin)
