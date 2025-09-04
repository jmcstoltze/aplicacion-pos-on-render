from django.db import models

from usuarios.models import Comuna

# Representa a un cliente del comercio
class Cliente(models.Model):
    """
    Modelo que representa a un cliente del comercio en el sistema POS.

    Almacena información personal, de contacto y ubicación de los clientes
    para gestión comercial, facturación y marketing.

    Attributes:
        rut (CharField): Rol Único Tributario (formato: XXXXXXXX-X)
            - Longitud: 12 caracteres máx.
            - No obligatoriamente único (puede repetirse para casos especiales)
        nombres (CharField): Nombres del cliente (80 chars máx.)
        ap_paterno (CharField): Apellido paterno (80 chars máx.)
        ap_materno (CharField): Apellido materno (80 chars máx.)
        telefono (CharField): Teléfono de contacto (20 chars máx.)
        email (EmailField): Correo electrónico (80 chars máx.)
        direccion (CharField): Dirección física (250 chars máx.)
        estado (BooleanField): Estado activo/inactivo del cliente
            - Default: True (activo al crear)
        comuna_id (ForeignKey): Relación con la comuna de residencia
            - SET_NULL si se elimina la comuna (null=True)
    
    Methods:
        __str__: Representación legible en formato "Apellidos, Nombres (RUT)"
        nombre_completo: Propiedad que devuelve el nombre completo formateado

    Meta:
        verbose_name: Configuración para interfaz administrativa
        ordering: Ordenamiento por defecto (apellido paterno, nombres)
        indexes: Índices para búsquedas frecuentes
    """
    
    rut = models.CharField(
        max_length=12, null=False, blank=False, unique=False,
        help_text="RUT en formato XX.XXX.XXX-X")
    nombres = models.CharField(
        max_length=80, null=False, blank=False,
        help_text="Nombres del cliente (ej: Juan Carlos)")
    ap_paterno = models.CharField(
        max_length=80, null=False, blank=False,
        help_text="Apellido paterno (ej: González)")
    ap_materno = models.CharField(
        max_length=80, null=False, blank=False,
        help_text="Apellido materno (ej: Pérez)")
    telefono = models.CharField(
        max_length=20, null=False, blank=False,
        help_text="Teléfono de contacto (+56912345678)")
    email = models.EmailField(
        max_length=80, null=False, blank=False,
        help_text="Correo electrónico válido (ej: cliente@dominio.com)")
    direccion = models.CharField(
        max_length=250, null=False, blank=False,
        help_text="Dirección completa (calle, número, depto)")
    estado = models.BooleanField(
        default=True, # Al crearse por defecto es True
        help_text="Cliente activo/inactivo")
    comuna_id = models.ForeignKey(
        Comuna, on_delete=models.SET_NULL, null=True,
        help_text="Comuna de residencia del cliente")
    
    def __str__(self):
        """Representación legible para selects/admin."""
        return f"{self.ap_paterno} {self.ap_materno}, {self.nombres} ({self.rut})"
    
    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['ap_paterno', 'ap_materno', 'nombres']  # Orden alfabético

# Representa a una empresa cliente que compra en el comercio
class Empresa(models.Model):
    """
    Modelo que representa una empresa cliente que realiza compras en el comercio.

    Registra información legal y comercial de empresas que son clientes del negocio,
    incluyendo sus datos tributarios, representante legal y ubicación geográfica.

    Attributes:
        nombre_empresa (CharField): Nombre comercial o de fantasía
            - Longitud: 150 caracteres
            - Requerido (null=False, blank=False)
        razon_social (CharField): Nombre legal registrado
            - Longitud: 250 caracteres
            - Único (unique=True)
            - Requerido
        giro (CharField): Actividad económica principal
            - Longitud: 150 caracteres
            - Requerido
        representante_id (ForeignKey): Relación con el representante legal
            - PROTECT: Evita eliminación si existe empresa asociada
            - Relación con modelo Cliente
        comuna_id (ForeignKey): Comuna de la empresa
            - PROTECT: Evita eliminación si existe empresa asociada
            - Relación con modelo Comuna

    Methods:
        __str__: Representación legible (nombre_empresa + razón social + representante)

    Meta:
        verbose_name: Configuración para interfaz administrativa
        ordering: Ordenamiento por defecto (nombre_empresa)
        indexes: Índices para búsquedas frecuentes
        constraints: Restricciones de validación
    """
    nombre_empresa = models.CharField(
        max_length=150, null=False, blank=False,
        help_text="Nombre de fantasía o marca (ej: 'Tech Solutions')")
    razon_social = models.CharField(
        max_length=250, null=False, blank=False, unique=True,
        help_text="Nombre legal registrado (ej: 'TECH SOLUTIONS S.A.')")
    giro = models.CharField(
        max_length=150, null=False, blank=False,
        help_text="Actividad económica principal (ej: 'VENTA EQUIPOS TECNOLÓGICOS')")
    representante_id = models.ForeignKey(
        Cliente, on_delete=models.PROTECT, # Eliminación protegida
        help_text="Cliente registrado como representante legal")
    comuna_id = models.ForeignKey(
        Comuna, on_delete=models.PROTECT, # Eliminación protegida
        help_text="Comuna de la empresa")
    
    def __str__(self):
        """Representación legible para selects/admin."""
        return (
            f"{self.razon_social}\n"
            f"Giro: {self.giro}\n"
            f"Representante: {self.representante_id}"
        )

    class Meta:
        verbose_name = "Empresa Cliente"
        verbose_name_plural = "Empresas Clientes"
        ordering = ['nombre_empresa']  # Orden alfabético

