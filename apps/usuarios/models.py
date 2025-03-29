from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Rol(models.Model):
    """
    Modelo para los diferentes roles del sistema
    """
    nombre = models.CharField(_('Nombre del rol'), max_length=50, unique=True)
    descripcion = models.TextField(_('Descripción'), blank=True)
    permisos = models.JSONField(_('Permisos'), default=dict, blank=True)
    activo = models.BooleanField(_('Activo'), default=True)
    fecha_creacion = models.DateTimeField(_('Fecha de creación'), auto_now_add=True)

    class Meta:
        verbose_name = _('Rol')
        verbose_name_plural = _('Roles')
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

class UsuarioManager(BaseUserManager):
    def create_user(self, nombre_usuario, password=None, **extra_fields):
        if not nombre_usuario:
            raise ValueError('El nombre de usuario es obligatorio')
        user = self.model(nombre_usuario=nombre_usuario, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, nombre_usuario, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(nombre_usuario, password, **extra_fields)

class Usuario(AbstractUser):
    # Cambia el campo de identificación
    USERNAME_FIELD = 'nombre_usuario'
    username = None  # Elimina el campo username por defecto
    nombre_usuario = models.CharField(_('Nombre de usuario'), max_length=30, unique=True)

    class Meta:
        swappable = 'AUTH_USER_MODEL'

    def __str__(self):
        return self.nombre_usuario

    def get_full_name(self):
        return self.nombre_usuario

    def get_short_name(self):
        return self.nombre_usuario