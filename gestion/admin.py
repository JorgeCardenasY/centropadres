from django.contrib import admin
from .models import Concepto, Pago
from centropadres.admin import my_admin_site

class PagoAdmin(admin.ModelAdmin):
    list_display = ('apoderado', 'concepto', 'monto', 'fecha_pago', 'registrado_por')
    list_filter = ('concepto', 'fecha_pago', 'apoderado')
    search_fields = ('apoderado__username', 'concepto__nombre')

my_admin_site.register(Concepto)
my_admin_site.register(Pago, PagoAdmin)