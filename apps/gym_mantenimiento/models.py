from django.db import models
from django.conf import settings  # Importación importante para AUTH_USER_MODEL

class Zona(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Zona'
        verbose_name_plural = 'Zonas'


class TipoIncidente(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Tipo de Incidente'
        verbose_name_plural = 'Tipos de Incidente'


class Urgencia(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Nivel de Urgencia'
        verbose_name_plural = 'Niveles de Urgencia'


class Maquina(models.Model):
    nombre = models.CharField(max_length=100)
    num_referencia = models.CharField(max_length=50, unique=True)
    peso = models.DecimalField(max_digits=10, decimal_places=2)  # Mejor que FloatField para pesos
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    garantia = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return f"{self.nombre} ({self.num_referencia})"

    class Meta:
        verbose_name = 'Máquina'
        verbose_name_plural = 'Máquinas'


class Solicitud(models.Model):
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('EN_PROCESO', 'En Proceso'),
        ('COMPLETADO', 'Completado'),
        ('CANCELADO', 'Cancelado'),
    ]
    
    zona = models.ForeignKey(Zona, on_delete=models.PROTECT)
    tipo_incidente = models.ForeignKey(TipoIncidente, on_delete=models.PROTECT)
    maquina = models.ForeignKey(Maquina, on_delete=models.PROTECT)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='PENDIENTE')
    descripcion = models.TextField()
    fecha_hora_ingreso = models.DateTimeField(auto_now_add=True)
    encargado = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Referencia correcta al modelo de usuario
        on_delete=models.PROTECT,
        related_name='solicitudes_asignadas'
    )
    fecha_hora_termino = models.DateTimeField(blank=True, null=True)
    urgencia = models.ForeignKey(Urgencia, on_delete=models.PROTECT)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Solicitud #{self.id} - {self.maquina.nombre}"

    class Meta:
        verbose_name = 'Solicitud'
        verbose_name_plural = 'Solicitudes'
        ordering = ['-fecha_hora_ingreso']