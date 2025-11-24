from django import forms
from .models import RegistroPago, Concepto, Deuda
from perfiles.models import Apoderado, Alumno

class RegistroPagoForm(forms.ModelForm):
    class Meta:
        model = RegistroPago
        fields = ['apoderado', 'alumno', 'concepto', 'monto_pagado', 'fecha', 'metodo_pago']
        widgets = {
            'fecha': forms.DateInput(attrs={'class': 'vDateField', 'type': 'date'}),
        }
        labels = {
            'apoderado': 'Apoderado',
            'alumno': 'Alumno',
            'concepto': 'Concepto Pagado',
            'monto_pagado': 'Monto',
            'fecha': 'Fecha',
            'metodo_pago': 'Medio de Pago',
        }

class ConceptoForm(forms.ModelForm):
    class Meta:
        model = Concepto
        fields = '__all__'
        widgets = {
            'fecha_limite': forms.DateInput(attrs={'class': 'vDateField', 'type': 'date'}),
        }

class AssignConceptForm(forms.Form):
    apoderado = forms.ModelChoiceField(queryset=Apoderado.objects.all(), label="Apoderado")
    concepto = forms.ModelChoiceField(queryset=Concepto.objects.all(), label="Concepto de Pago")


