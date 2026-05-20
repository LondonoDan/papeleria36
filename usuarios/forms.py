from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Perfil


class LoginForm(forms.Form):
    username = forms.CharField(
        label='Usuario',
        widget=forms.TextInput(attrs={'placeholder': 'Nombre de usuario'})
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'})
    )


class CrearUsuarioForm(UserCreationForm):
    email = forms.EmailField(required=False, label='Correo electrónico')
    rol = forms.ChoiceField(
        choices=Perfil.ROL_CHOICES,
        label='Rol'
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'rol']




class EditarUsuarioForm(forms.ModelForm):
    rol = forms.ChoiceField(choices=Perfil.ROL_CHOICES, label='Rol')

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and hasattr(self.instance, 'perfil'):
            self.fields['rol'].initial = self.instance.perfil.rol