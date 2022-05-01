import hashlib as hb
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import UserManager

class User(AbstractBaseUser, PermissionsMixin):
    MALE            = 'MALE'
    FEMALE          = 'FEMALE'
    OTHER           = 'OTHER'
    GENDER_CHOICES  = [
    (MALE, 'male'),
    (FEMALE, 'female'),
    (OTHER, 'other'),
    ]

    username        = models.CharField(max_length=100, unique=True)
    first_name      = models.CharField(max_length=100)
    last_name       = models.CharField(max_length=100)
    country         = models.CharField(max_length=50)
    birthday        = models.DateField(default=timezone.now)
    email           = models.EmailField(_('email address'))
    gender          = models.CharField(
                                max_length=50,
                                choices=GENDER_CHOICES,
                                default=OTHER)
    phone           = models.CharField(max_length=100)
    check_unity     = models.CharField(max_length=200, default="")
    status          = models.BooleanField(max_length=200, default=False)

    date_joined     = models.DateTimeField(default=timezone.now)
    is_superuser    = models.BooleanField(default=False)
    is_active       = models.BooleanField(default=False)
    is_staff        = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'country', 'birthday', 'email', 'gender', 'phone',]

    objects = UserManager()

    @staticmethod
    def hash_unity_password(password):
        salt = "2012412313154"
        toHash = (password + salt).encode('UTF-8')
        hshpass = (hb.md5(toHash).hexdigest()).upper()
        return hshpass

    def __str__(self):
        return self.username

    def unity_hash(self):
        return self.check_unity


    def has_staff_permits(self):
        return self.is_staff

    def has_superuser_permits(self):
        return self.is_superuser

    def logged_in(self):
        return self.is_active

class Canciones(models.Model):
    Nombre= models.CharField(max_length=50)
    Duracion = models.CharField(max_length=30)
    Genero= models.CharField(max_length=30)
    Ritmo= models.CharField(max_length=30)
    Dificultad = models.CharField(max_length=30)

class Historial(models.Model):
    Nombre_usuario= models.CharField(max_length=50)
    #Nombre_usuario= models.CharField(Usuarios, on_delete=models.CASCADE)
    ID_Usuario= models.CharField(max_length=30)
    Puntos_por_partida= models.CharField(max_length=30)
    Fecha_del_juego= models.CharField(max_length=30)
    ID_Canciones= models.CharField(max_length=30)
    Tiempo_jugado = models.CharField(max_length=30)
    
