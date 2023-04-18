from django.db import models
from django.contrib.auth.models import BaseUserManager

class UserManager (BaseUserManager, models.Manager):
    
    # _create_user, funcion privada
    def _create_user(self, username, email, password, is_staff, is_superuser, **extra_fields):
        user = self.model(
            username = username,
            email = email,            
            is_staff = is_staff, # Si puede acceder al administrador de Django
            is_superuser = is_superuser,
            **extra_fields
        )
        user.set_password(password) # encripta el password
        user.save(using = self.db) # especifica en que bd se guarda
        return user
    
    def create_user(self, username, email, password=None, is_staff=False, **extra_fields):
        print(is_staff)
        return self._create_user(username, email, password, is_staff, is_superuser=False, **extra_fields)
    
    def create_superuser(self, username, email, password=None, **extra_fields):
        return self._create_user(username, email, password, is_staff=True, is_superuser=True, **extra_fields)
