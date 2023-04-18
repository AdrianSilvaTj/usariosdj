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
    
    def __init__(self, username, *args, **kwargs):
        """ Se le indica al formulario que en su inicialización se le pasara un nueva parametro 'username' 
        y este se va a guardar en self.username """
        self.username = username
        super(PasswordUpdateForm, self).__init__(*args, **kwargs)
    
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
    
    def clean(self):
        #Se autentica el usuario, para verificar que se ingresó el password correcto
        user_auth = authenticate(
            username=self.username,
            password=self.cleaned_data['password1']
        )
        if not user_auth:
            raise forms.ValidationError("La contraseña Actual es incorrecta")
    
class VerificationForm(forms.Form):
    code_ver = forms.CharField(
        label='Ingrese el código enviado',
        required=True,        
    )
    
    def __init__(self, pk, *args, **kwargs):
        """ Se le indica al formulario que en su inicialización se le pasara un nueva parametro 'pk' 
        y este se va a guardar en id_user """
        self.id_user = pk
        super(VerificationForm, self).__init__(*args, **kwargs)
        
    
    def clean_code_ver(self):
        code = self.cleaned_data['code_ver']
        
        if len(code) == 6:
            # Verificamos si el id y el codigo enviado son validos
            active = User.objects.code_validation(
                self.id_user,
                code
            )
            if not active:
                raise forms.ValidationError("El código es incorrecto")
                        
        else:
            raise forms.ValidationError("El código es incorrecto")
        