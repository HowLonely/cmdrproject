from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

class Rol(models.Model):
    """
    Modelo para los diferentes roles del sistema
    """
    nombre = models.CharField(_('Nombre del rol'), max_length=50, unique=True)
    descripcion = models.TextField(_('Descripción'), blank=True)
    permisos = models.ManyToManyField(
        'auth.Permission',
        verbose_name=_('Permisos'),
        blank=True,
        help_text=_('Permisos específicos para este rol')
    )
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
        
        # Forzar rol si no se especifica
        if 'rol' not in extra_fields:
            extra_fields.setdefault('rol', Rol.objects.get(nombre='TECNICO'))
            
        user = self.model(nombre_usuario=nombre_usuario, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, nombre_usuario, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('rol', Rol.objects.get_or_create(nombre='ADMIN')[0])
        return self.create_user(nombre_usuario, password, **extra_fields)

class Usuario(AbstractUser):
    username = None  # Eliminamos el campo username por defecto
    nombre_usuario = models.CharField(
        _('Nombre de usuario'),
        max_length=30,
        unique=True,
        help_text=_('Requerido. 30 caracteres o menos. Letras, dígitos y @/./+/-/_ solamente.')
    )
    rol = models.ForeignKey(
        Rol,
        on_delete=models.PROTECT,
        verbose_name=_('Rol'),
        related_name='usuarios'
    )
    
    USERNAME_FIELD = 'nombre_usuario'
    REQUIRED_FIELDS = []  # Eliminamos 'email' si no es requerido

    objects = UsuarioManager()

    def __str__(self):
        return f"{self.nombre_usuario} ({self.rol.nombre})"

    @property
    def es_encargado(self):
        return self.rol.nombre == 'ENCARGADO'

    @property
    def es_tecnico(self):
        return self.rol.nombre == 'TECNICO'

    @property
    def es_admin(self):
        return self.is_superuser or self.rol.nombre == 'ADMIN'

    class Meta:
        verbose_name = _('Usuario')
        verbose_name_plural = _('Usuarios')
        swappable = 'AUTH_USER_MODEL'