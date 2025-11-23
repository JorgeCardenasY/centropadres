from django import forms
from .models import RegistroPago

class RegistroPagoForm(forms.ModelForm):
    class Meta:
        model = RegistroPago
        fields = '__all__'
        labels = {
            'concepto': 'Tipo Deuda',
            'monto_pagado': 'Ingrese Monto',
        }
