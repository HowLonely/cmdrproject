from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from .models import Rol, Usuario

@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'activo', 'fecha_creacion')
    list_filter = ('activo',)
    search_fields = ('nombre', 'descripcion')
    filter_horizontal = ('permisos',)  # Para selección más fácil de permisos
    fieldsets = (
        (None, {
            'fields': ('nombre', 'descripcion', 'activo')
        }),
        ('Permisos', {
            'fields': ('permisos',),
            'classes': ('collapse', 'wide')
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            # Opcional: Filtrar roles visibles para usuarios no super
            qs = qs.filter(activo=True)
        return qs
    
class UsuarioAdmin(UserAdmin):
    # Campos a mostrar en la lista
    list_display = ('nombre_usuario', 'email', 'rol', 'is_active', 'is_staff')
    list_filter = ('rol', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('nombre_usuario', 'email', 'first_name', 'last_name')
    ordering = ('nombre_usuario',)
    
    # Campos en el formulario de edición
    fieldsets = (
        (None, {'fields': ('nombre_usuario', 'password')}),
        ('Información personal', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Roles y permisos', {
            'fields': ('rol', 'is_active', 'is_staff', 'is_superuser', 
                      'groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
        ('Fechas importantes', {
            'fields': ('last_login', 'date_joined'),
            'classes': ('collapse',)
        }),
    )
    
    # Campos al agregar nuevo usuario
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('nombre_usuario', 'password1', 'password2', 'rol'),
        }),
    )
    
    # Filtrado personalizado
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(is_superuser=False)
        return qs
    
    # Acciones personalizadas
    actions = ['activar_usuarios', 'desactivar_usuarios']
    
    def activar_usuarios(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} usuarios activados")
    activar_usuarios.short_description = "Activar usuarios seleccionados"
    
    def desactivar_usuarios(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} usuarios desactivados")
    desactivar_usuarios.short_description = "Desactivar usuarios seleccionados"

# Registrar el modelo Usuario con la configuración personalizada
admin.site.register(Usuario, UsuarioAdmin)