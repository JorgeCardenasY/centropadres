from django.contrib import admin
from .models import Concepto, RegistroPago, Deuda
from perfiles.models import Apoderado, Alumno
from .forms import RegistroPagoForm
from centropadres.admin import my_admin_site

class ConceptoAdmin(admin.ModelAdmin):
    actions = ['asignar_a_todos_los_apoderados']

    def asignar_a_todos_los_apoderados(self, request, queryset):
        for concepto in queryset:
            # Get all Apoderados that have at least one Alumno
            apoderados = Apoderado.objects.filter(alumnos__isnull=False).distinct()
            for apoderado in apoderados:
                for alumno in apoderado.alumnos.all():
                    Deuda.objects.get_or_create(
                        apoderado=apoderado,
                        alumno=alumno,
                        concepto=concepto
                    )
        self.message_user(request, f"Conceptos asignados a todos los apoderados con alumnos.")
    
    asignar_a_todos_los_apoderados.short_description = "Asignar concepto a todos los apoderados"

    class Media:
        js = (
            'admin/js/vendor/jquery/jquery.js',
            'admin/js/calendar.js',
            'admin/js/admin/DateTimeShortcuts.js'
        )
        css = {
            'all': ('admin/css/widgets.css',)
        }

class RegistroPagoAdmin(admin.ModelAdmin):
    form = RegistroPagoForm
    list_display = ('apoderado', 'alumno', 'concepto', 'monto_pagado', 'fecha', 'registrador')
    list_filter = ('concepto', 'fecha', 'apoderado')
    search_fields = ('apoderado__nombres', 'alumno__nombres', 'concepto__nombre')
    exclude = ('deuda',)
    readonly_fields = ('registrador',)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not obj:  # Only for add form
            try:
                # Get the Apoderado instance of the logged-in user
                registrador = request.user.apoderado
                if registrador.registrar_pago:
                    form.base_fields['registrador'].initial = registrador
            except Apoderado.DoesNotExist:
                pass
        return form

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "registrador":
            kwargs["queryset"] = Apoderado.objects.filter(registrar_pago=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    class Media:
        js = ('js/admin/filter_alumnos.js',)

my_admin_site.register(Concepto, ConceptoAdmin)
my_admin_site.register(RegistroPago, RegistroPagoAdmin)
my_admin_site.register(Deuda)