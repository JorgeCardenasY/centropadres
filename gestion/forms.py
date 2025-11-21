from django import forms
from .models import Pago

class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = ('apoderado', 'concepto', 'monto', 'fecha_pago')
        widgets = {
            'fecha_pago': forms.DateInput(attrs={'type': 'date'}),
        }
