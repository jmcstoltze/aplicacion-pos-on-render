from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.http import HttpResponse
import csv
from .models import Region, Comuna, Rol, Usuario

# ==================== REGION & COMUNA ====================
@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('nombre_region',)
    search_fields = ('nombre_region',)
    ordering = ('nombre_region',)

@admin.register(Comuna)
class ComunaAdmin(admin.ModelAdmin):
    list_display = ('nombre_comuna', 'region')
    list_filter = ('region',)
    search_fields = ('nombre_comuna', 'region__nombre_region')
    ordering = ('nombre_comuna',)

# ==================== ROL ====================
@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ('nombre_rol', 'descripcion')
    search_fields = ('nombre_rol',)
    list_filter = ('nombre_rol',)

# ==================== USUARIO ====================
class UsuarioInline(admin.StackedInline):
    model = Usuario
    can_delete = False
    verbose_name_plural = 'Información adicional'
    fk_name = 'usuario'

class CustomUserAdmin(UserAdmin):
    inlines = (UsuarioInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_rut', 'get_rol')
    list_select_related = ('usuario',)

    def get_rut(self, instance):
        return instance.usuario.rut
    get_rut.short_description = 'RUT'

    def get_rol(self, instance):
        return instance.usuario.rol.nombre_rol if hasattr(instance, 'usuario') and instance.usuario.rol else '-'
    get_rol.short_description = 'Rol'

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super().get_inline_instances(request, obj)

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('rut', 'nombres', 'ap_paterno', 'ap_materno', 'usuario', 'rol', 'estado')
    list_filter = ('rol', 'estado', 'comuna__region')
    search_fields = ('rut', 'nombres', 'ap_paterno', 'ap_materno', 'usuario__username')
    ordering = ('ap_paterno', 'ap_materno', 'nombres')
    raw_id_fields = ('usuario',)
    actions = ['export_to_csv']

    fieldsets = (
        (None, {
            'fields': ('usuario', 'rut', 'estado')
        }),
        ('Información personal', {
            'fields': ('nombres', 'ap_paterno', 'ap_materno', 'email', 'telefono')
        }),
        ('Dirección', {
            'fields': ('direccion', 'comuna')
        }),
        ('Roles y permisos', {
            'fields': ('rol',)
        }),
    )

    def export_to_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="usuarios_pos.csv"'
        response.write('\ufeff')  # BOM para UTF-8

        writer = csv.writer(response)
        writer.writerow([
            'RUT', 'Nombres', 'Apellido Paterno', 'Apellido Materno', 
            'Teléfono', 'Email', 'Dirección', 'Comuna', 'Región', 'Rol', 'Estado'
        ])

        for usuario in queryset:
            writer.writerow([
                usuario.rut,
                usuario.nombres,
                usuario.ap_paterno,
                usuario.ap_materno,
                usuario.telefono,
                usuario.email,
                usuario.direccion,
                usuario.comuna.nombre_comuna if usuario.comuna else '',
                usuario.comuna.region.nombre_region if usuario.comuna else '',
                usuario.rol.nombre_rol,
                'Activo' if usuario.estado else 'Inactivo'
            ])

        return response
    export_to_csv.short_description = "Exportar a CSV"

# Desregistrar el UserAdmin por defecto y registrar el personalizado
from django.contrib.auth.models import User
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)