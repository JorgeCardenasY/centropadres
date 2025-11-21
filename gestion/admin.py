from django.contrib import admin
from .models import Concepto, Pago

class PagoAdmin(admin.ModelAdmin):
    list_display = ('apoderado', 'concepto', 'monto', 'fecha_pago', 'registrado_por')
    list_filter = ('concepto', 'fecha_pago', 'apoderado')
    search_fields = ('apoderado__username', 'concepto__nombre')

admin.site.register(Concepto)
admin.site.register(Pago, PagoAdmin)