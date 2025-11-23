from django.contrib import admin
from .models import Concepto, RegistroPago
from perfiles.models import Apoderado
from .forms import RegistroPagoForm
from centropadres.admin import my_admin_site

class RegistroPagoAdmin(admin.ModelAdmin):
    form = RegistroPagoForm
    list_display = ('apoderado', 'alumno', 'concepto', 'monto_pagado', 'fecha', 'registrador')
    list_filter = ('concepto', 'fecha', 'apoderado')
    search_fields = ('apoderado__nombres', 'alumno__nombres', 'concepto__nombre')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "registrador":
            kwargs["queryset"] = Apoderado.objects.filter(registrar_pago=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    class Media:
        js = ('js/admin/filter_alumnos.js',)

my_admin_site.register(Concepto)
my_admin_site.register(RegistroPago, RegistroPagoAdmin)