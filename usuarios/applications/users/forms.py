from django import forms
from django.contrib.auth import authenticate

from .models import User

class UserRegisterForm(forms.ModelForm):
    """ Estructura del Form de Registro de Usuario """
    password1 = forms.CharField(
        label='Contraseña',
        required=True,
        widget = forms.PasswordInput(
            attrs={
                'placeholder': 'Contraseña'
            }
        )
    )
    password2 = forms.CharField(
        label='Contraseña',
        required=True,
        widget = forms.PasswordInput(
            attrs={
                'placeholder': 'Repetir Contraseña'
            }
        )
    )
    
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'gender',
            'is_staff',
            'is_active'
        )
    
    def clean_password2(self):
        """ Verificar que las contraseñas coincidan """
        if self.cleaned_data['password1'] != self.cleaned_data['password2']:
            self.add_error('password2', 'Las Contraseñas no son las mismas')

class LoginForm(forms.Form):
    """ Estructura del Form de Login de Usuario """
    username = forms.CharField(
        label='Usuario',
        required=True,
        widget = forms.TextInput(
            attrs={
                'placeholder': 'Username'
            }
        )
    )
    password = forms.CharField(
        label='Contraseña',
        required=True,
        widget = forms.PasswordInput(
            attrs={
                'placeholder': 'Contraseña'
            }
        )
    )
    
    def clean(self):
        """ Aca se validara que existan los datos del usuario ingresado """
        cleaned_data = super(LoginForm, self).clean() # Para poder retornar todos los datos del formulario
        userauth = authenticate(
            username=cleaned_data['username'],
            password=cleaned_data['password']
        )
        if not userauth:
            raise forms.ValidationError("Los datos del usuario no son correctos")
        else:
            cleaned_data['user']= userauth
            
        return cleaned_data
    
class PasswordUpdateForm(forms.Form):
    password1 = forms.CharField(
        label='Contraseña Actual',
        required=True,
        widget = forms.PasswordInput(
            attrs={
                'placeholder': 'Contraseña'
            }
        )
    )
    password2 = forms.CharField(
        label='Contraseña Nueva',
        required=True,
        widget = forms.PasswordInput(
            attrs={
                'placeholder': 'Contraseña'
            }
        )
    )
    
class VerificationForm(forms.Form):
    password1 = forms.CharField(
        label='Ingrese el código enviado',
        required=True,        
    )