from django.db import models
from django.contrib.auth.models import User

# Región de la dirección del usuario o del cliente
class Region(models.Model):
    """
    Modelo que representa la Región geográfica.

    Attributes:
        nombre_region (CharField): Nombre de la región. 
            Campo obligatorio con una longitud máxima de 80 caracteres.

    Meta:
        verbose_name (str): Nombre singular para mostrar en la interfaz admin.
        verbose_name_plural (str): Nombre plural para mostrar en la interfaz admin.
        ordering (list): Ordenamiento por defecto (alfabético por nombre_region).

    Methods:
        __str__: Representación en string del modelo (devuelve el nombre_region).
    """
    nombre_region = models.CharField(max_length=80, null=False, blank=False)

    def __str__(self):
        return self.nombre_region
    
    class Meta:
        verbose_name = "Region"
        verbose_name_plural = "Regiones"
        ordering = ["nombre_region"]

# Comuna de la dirección del usuario o del cliente
class Comuna(models.Model):
    """
    Modelo que representa la Comuna dentro del sistema.

    La Comuna pertenece a una Región específica
    y se utiliza para registrar direcciones de usuarios o clientes.

    Attributes:
        nombre_comuna (CharField): Nombre de la comuna. Campo obligatorio con
            una longitud máxima de 80 caracteres.
        region (ForeignKey): Relación con el modelo Region. Campo obligatorio que
            protege contra la eliminación de la Región si existen Comunas asociadas.

    Methods:
        __str__: Representación en cadena de texto que devuelve el nombre de la comuna.

    Meta:
        verbose_name: Nombre singular para mostrar en la interfaz de administración.
        verbose_name_plural: Nombre plural para mostrar en la interfaz de administración.
        ordering: Ordenamiento predeterminado por nombre_comuna (orden alfabético).
    """
    nombre_comuna = models.CharField(max_length=80, null=False, blank=False)
    region = models.ForeignKey(Region, null=False, blank=False, on_delete=models.PROTECT) # No se puede eliminar región sin eliminar las comunas asociadas

    def __str__(self):
        return self.nombre_comuna
    
    class Meta:
        verbose_name = "Comuna"
        verbose_name_plural = "Comunas"
        ordering = ["nombre_comuna"]

# Rol del usuario
class Rol(models.Model):
    """
    Modelo que representa los roles de usuarios en el sistema POS.
    
    Los roles definen los permisos y funcionalidades accesibles para cada tipo de usuario
    (Administrador, Jefe de Local y Cajero).
    
    Attributes:
        nombre_rol (CharField): Nombre del rol (único en el sistema). Ej: 'Administrador'.
        descripcion (CharField): Explicación detallada del rol y sus capacidades.
    """

    ADMINISTRADOR = 'Administrador'
    JEFE_LOCAL = 'Jefe de local'
    CAJERO = 'Cajero'

    ROLES_CHOICES = [
        (ADMINISTRADOR, 'Administrador'),
        (JEFE_LOCAL, 'Jefe de local'),
        (CAJERO, 'Cajero'),
    ]

    nombre_rol = models.CharField(
        max_length=80, null=False, blank=False, unique=True,
        choices=ROLES_CHOICES,
        help_text="Nombre identificador del rol (Administrador, Jefe de local o Cajero)"
    )
    
    descripcion = models.CharField(
        max_length=250,
        help_text="Descripción detallada de las funciones asociadas al rol"
    )
    
    def __str__(self):
        """
        Representación legible del rol (usado en admin/interfaz).
        
        Returns:
            str: Nombre del rol en formato humano.
        """
        return self.nombre_rol
    
    class Meta:
        """
        Metadata adicional para el modelo.
        
        Attributes:
            verbose_name (str): Nombre singular para interfaces administrativas.
            verbose_name_plural (str): Nombre plural para interfaces administrativas.
            ordering (list): Criterio de ordenación por defecto en consultas.
        """
        verbose_name = "Rol"
        verbose_name_plural = "Roles"
        ordering = ["id"]
        
# Usuario de la aplicación, puede ser Administrador, Jefe de local o Cajero
class Usuario(models.Model):
    """
    Modelo que representa a un usuario del sistema POS con información personal extendida.
    
    Extiende el modelo User de Django mediante relación OneToOne, añadiendo datos específicos
    como RUT, nombres completos y datos de contacto. Se utiliza para todos los perfiles
    (Administradores, Jefes de Local y Cajeros).

    Attributes:
        rut (CharField): Identificador único
        nombres (CharField): Nombres del usuario.
        ap_paterno (CharField): Apellido paterno.
        ap_materno (CharField): Apellido materno.
        telefono (CharField): Número de contacto.
        email (CharField): Correo electrónico.
        direccion (CharField): Dirección física completa.
        usuario (OneToOneField): Relación con el modelo User de Django para autenticación.
        estado (BooleanField): Estado del usuario (activo o eliminado).
        rol (ForeignKey): Referencia al rol (Administrador, Jefe de Local, Cajero).
        comuna (FOreignKey): Referencia a la comuna de la dirección. NULLABLE.
    """    
    rut = models.CharField(
        max_length=12, null=False, blank=False, unique=True,
        help_text="RUT en formato 12345678-9 (incluye guión y dígito verificador)")
    
    nombres = models.CharField(
        max_length=80, null=False, blank=False,
        help_text="Nombres del usuario")
    
    ap_paterno = models.CharField(
        max_length=80, null=False, blank=False,
        help_text="Apellido paterno")
    
    ap_materno = models.CharField(
        max_length=80, null=False, blank=False,
        help_text="Apellido materno")
    
    telefono = models.CharField(
        max_length=20, null=False, blank=False,
        help_text="Número de contacto en formato +56912345678")
    
    email = models.EmailField(
        max_length=80, null=False, blank=False,
        help_text="Correo electrónico válido (será usado para notificaciones)")
    
    direccion = models.CharField(
        max_length=250, null=False, blank=False,
        help_text="Dirección completa: Calle, número, [depto/villa/población/bloque] (opcional)")
    
    estado = models.BooleanField(
        default=True,
        verbose_name="Activo",
        help_text="Indica si el registro está activo o eliminado")
    
    usuario = models.OneToOneField(
        User, on_delete=models.PROTECT, # Eliminación protegida
        help_text="Usuario de autenticación asociado (auth.User)")
    
    rol = models.ForeignKey(
        Rol, on_delete=models.PROTECT, # Eliminación protegida
        help_text="Rol del usuario (Administrador, Jefe de local o Cliente)")
    
    comuna = models.ForeignKey(
        Comuna, on_delete=models.SET_NULL, # Si se elimina la comuna, establece NULL
        null=True, blank=True,
        help_text="Comuna de la dirección del usuario (opcional)")

    def __str__(self):
        """
        Representación legible del usuario para interfaces administrativas.
        
        Returns:
            str: Cadena en formato "RUT | Apellidos | Nombres | Username".
        """
        return f"{self.rut} | {self.ap_paterno} | {self.ap_materno} | {self.nombres} | {self.usuario.username} | [{'Activo' if self.estado else 'Eliminado'}]"
    
    class Meta:
        """
        Configuración metadata para el modelo Usuario.
        
        Attributes:
            verbose_name (str): Nombre singular en interfaces administrativas.
            verbose_name_plural (str): Nombre plural en interfaces administrativas.
            ordering (list): Criterio de ordenación por defecto [rut, apellidos, nombres].
        """
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        ordering = ["rut", "ap_paterno", "ap_materno", "nombres", "usuario__last_name"]
