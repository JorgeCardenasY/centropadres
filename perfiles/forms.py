from django import forms
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from django.contrib.auth.models import User
from .models import Perfil

class UserCreationForm(BaseUserCreationForm):
    class Meta(BaseUserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ('user', 'rol')
