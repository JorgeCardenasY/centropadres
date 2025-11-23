from django import forms
from .models import RegistroPago

class RegistroPagoForm(forms.ModelForm):
    class Meta:
        model = RegistroPago
        fields = '__all__'
