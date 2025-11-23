from django.contrib import admin
from .models import Concepto, RegistroPago
from centropadres.admin import my_admin_site

class RegistroPagoAdmin(admin.ModelAdmin):
    list_display = ('apoderado', 'alumno', 'concepto', 'monto_pagado', 'fecha', 'registrador')
    list_filter = ('concepto', 'fecha', 'apoderado')
    search_fields = ('apoderado__nombres', 'alumno__nombres', 'concepto__nombre')

my_admin_site.register(Concepto)
my_admin_site.register(RegistroPago, RegistroPagoAdmin)