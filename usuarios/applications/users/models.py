from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager

class User(AbstractBaseUser, PermissionsMixin):
    """ Modelo para manejar todo lo relacionado con los Usuarios incluso los Superusuarios """
    
    GENDER_CHOICES = (
        ('M','Masculino'),
        ('F','Femenino'),
    )
    
    username = models.CharField("Nombre de Usuario", max_length=50, unique=True)
    email = models.EmailField()
    first_name = models.CharField("Nombres", max_length=50, blank=True)
    last_name = models.CharField("Apellidos", max_length=50, blank=True)
    gender = models.CharField("Genero", max_length=1, choices=GENDER_CHOICES, blank=True)
    cod_register = models.CharField(max_length=6, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active =  models.BooleanField(default=True)

    # Campos requeridos por el AbstractBaseUser, USERNAME_FIELD, campo para el nombre de usuario
    # REQUIRED_FIELDS, otros campos que se pediran en la creación de usuarios
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = [ 'email',]
    
    objects = UserManager()
    
    def __str__(self):
        return str(self.id) + '-' + self.get_short_name()    
    
    def get_short_name(self):
        return self.username
    
    def get_full_name(self):
        return self.first_name + ' ' + self.last_name