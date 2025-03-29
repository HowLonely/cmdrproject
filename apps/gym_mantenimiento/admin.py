# gym_mantenimiento/admin.py
from django.contrib import admin
from .models import Zona, TipoIncidente, Urgencia, Maquina, Solicitud

@admin.register(Zona)
class ZonaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)
    ordering = ('nombre',)

@admin.register(TipoIncidente)
class TipoIncidenteAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)
    ordering = ('nombre',)

@admin.register(Urgencia)
class UrgenciaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)
    ordering = ('nombre',)

@admin.register(Maquina)
class MaquinaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'num_referencia', 'marca', 'modelo', 'garantia')
    search_fields = ('nombre', 'num_referencia', 'marca', 'modelo')
    list_filter = ('marca',)
    ordering = ('nombre',)
    fieldsets = (
        (None, {
            'fields': ('nombre', 'num_referencia')
        }),
        ('Detalles técnicos', {
            'fields': ('peso', 'marca', 'modelo'),
            'classes': ('collapse',)
        }),
        ('Garantía', {
            'fields': ('garantia',),
            'classes': ('wide',)
        }),
    )

@admin.register(Solicitud)
class SolicitudAdmin(admin.ModelAdmin):
    list_display = ('id', 'maquina', 'zona', 'tipo_incidente', 'estado', 'urgencia', 'encargado', 'fecha_hora_ingreso')
    list_filter = ('estado', 'urgencia', 'zona', 'tipo_incidente')
    search_fields = ('maquina__nombre', 'descripcion', 'encargado__username')
    date_hierarchy = 'fecha_hora_ingreso'
    ordering = ('-fecha_hora_ingreso',)
    raw_id_fields = ('maquina', 'encargado')
    readonly_fields = ('fecha_hora_ingreso', 'updated_at')
    
    fieldsets = (
        (None, {
            'fields': ('maquina', 'zona', 'tipo_incidente', 'urgencia', 'encargado')
        }),
        ('Estado', {
            'fields': ('estado', 'descripcion')
        }),
        ('Fechas', {
            'fields': ('fecha_hora_ingreso', 'fecha_hora_termino', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(encargado=request.user)
        return qs