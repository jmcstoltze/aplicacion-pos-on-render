from django.db import models
from django.core.validators import MinValueValidator

from usuarios.models import Comuna, Usuario

# Representa al comercio involucrado en el negocio
class Comercio(models.Model):
    """
    Modelo que representa un Comercio o establecimiento comercial en el sistema.

    Almacena información básica del comercio incluyendo sus datos de contacto
    y denominaciones legales. Se utiliza para gestionar la relación con clientes,
    proveedores o transacciones.

    Attributes:
        nombre_comercio (CharField): Nombre de fantasía o público del comercio.
        razon_social (CharField): Nombre legal registrado (debe ser único en el sistema).
        email (EmailField): Correo electrónico corporativo válido.
        telefono (CharField): Número de contacto en formato internacional.

    Methods:
        __str__: Representación legible del comercio (devuelve nombre_comercio + razón social).

    Meta:
        verbose_name: Nombre singular para la interfaz administrativa.
        verbose_name_plural: Nombre plural para la interfaz administrativa.
        ordering: Ordenamiento por defecto (nombre_comercio ascendente).
        indexes: Índice para mejorar búsquedas por razón social.
        constraints: Restricción de unicidad para email corporativo.
    """

    nombre_comercio = models.CharField(
        max_length=160, null=False, blank=False,
        help_text="Nombre de fantasía del comercio")
    razon_social = models.CharField(
        max_length=250, null=False, blank=False, unique=True,
        help_text="Razón social o nombre legal del comercio")
    email = models.EmailField(
        max_length=80, null=False, blank=False,
        help_text="Correo electrónico válido corporativo para el comercio")
    telefono = models.CharField(
        max_length=20, null=False, blank=False,
        help_text="Número de contacto en formato +56912345678")

    def __str__(self):
        """Representación legible."""
        return f"{self.nombre_comercio} | {self.razon_social}"

    class Meta:
        verbose_name = "Comercio"
        verbose_name_plural = "Comercios"
        ordering = ["nombre_comercio"]
   
# Representa a las sucursales que posee el comercio
class Sucursal(models.Model):
    """
    Modelo que representa una sucursal física perteneciente a un Comercio.

    Cada sucursal tiene información de contacto, ubicación geográfica y estados operativos.
    Se relaciona con un Comercio principal y una Comuna específica.

    Attributes:
        nombre_sucursal (CharField): Nombre identificatorio único de la sucursal (80 chars).
        email (EmailField): Correo electrónico corporativo válido.
        telefono (CharField): Teléfono en formato internacional (+56912345678).
        dirección (CharField): Dirección de la sucursal.
        es_casa_matriz (BooleanField): Indica si es la sede principal del comercio.
        esta_asignada (BooleanField): Indica si la sucursal tiene asignación operativa.
        jefe_asignado (IntegerField): Indica el jefe de local al cual se le asigna la sucursal.
        estado (BooleanField): Estado activo/inactivo de la sucursal.
        comercio (ForeignKey): Relación con el Comercio al que pertenece.
        comuna (ForeignKey): Ubicación geográfica referencial.

    Methods:
        __str__: Representación legible en formato: [CASA MATRIZ] Nombre (Comercio).

    Meta:
        verbose_name: Configuración para la interfaz administrativa.
        ordering: Ordenamiento predeterminado de registros.
    """

    nombre_sucursal = models.CharField(
        max_length=80, null=False, blank=False, unique=True,
        help_text="Nombre referencial o identificatorio de la sucursal ")
    email = models.EmailField(
        max_length=80, null=False, blank=False,
        help_text="Correo electrónico válido corporativo para la sucursal")
    telefono = models.CharField(
        max_length=20, null=False, blank=False,
        help_text="Número de contacto en formato +56912345678")
    direccion = models.CharField(
        max_length=250, null=False, blank=False,
        help_text="Dirección de la sucursal")
    es_casa_matriz = models.BooleanField(
        default=False, # No casa matriz por defecto
        verbose_name = "Casa Matriz",
        help_text="Indica si la sucursal es casa matriz o no")
    esta_asignada = models.BooleanField(
        default=False, # No asignada por defecto
        verbose_name = "Asignada",
        help_text="Indica si la sucursal está asignada o no")
    jefe_asignado = models.OneToOneField(
        Usuario, on_delete=models.PROTECT,
        null=True,
        blank=True,
        help_text="Jefe de local al cual se le asigna la sucursal")
    estado = models.BooleanField(
        default=True, # Activa por defecto
        verbose_name = "Activa",
        help_text="Indica si la sucursal está activa o no")
    comercio = models.ForeignKey(
        Comercio, on_delete=models.PROTECT, # Eliminación protegida
        help_text="Comercio que lidera el conjunto de sucursales",
        related_name="sucursales")
    comuna = models.ForeignKey(
        Comuna, on_delete=models.PROTECT, # Eliminación protegida
        help_text="Comuna de la dirección de la sucursal",
        related_name="comuna")
    
    def __str__(self):
        """Representación legible que incluye estado de casa matriz."""
        matriz_flag = "[CASA MATRIZ] " if self.es_casa_matriz else ""
        return f"{matriz_flag}{self.nombre_sucursal}"

    class Meta:
        verbose_name = "Sucursal"
        verbose_name_plural = "Sucursales"
        ordering = ["-es_casa_matriz", "nombre_sucursal"]  # Casa matriz primero

# Representa a las bodegas asociadas a cada sucursal
class Bodega(models.Model):
    """
    Modelo que representa una bodega en el sistema.

    Attributes:
        nombre_bodega (CharField): Nombre de la bodega. 
            - Obligatorio (null=False, blank=False)
            - Único (unique=True)
            - Longitud máxima: 80 caracteres
        es_principal (BooleanField): Indica si es la bodega principal.
            - Por defecto: False
            - El verbose_name está configurado como negación para mejor legibilidad
        sucursal_id (ForeignKey): Relación con la sucursal a la que pertenece la bodega.
            - Relación con el modelo Sucursal
            - On_delete: SET_NULL (si se elimina la sucursal, este campo se establece a NULL)
            - Puede ser nulo (null=True)

    Methods:
        __str__: Devuelve la representación en string del modelo (nombre de la bodega)

    Meta:
        verbose_name = 'Bodega'
        verbose_name_plural = 'Bodegas'
        ordering = ['nombre_bodega']  # Ejemplo de ordenación por defecto
    """
    nombre_bodega = models.CharField(
        max_length=80, null=False, blank=False, unique=True,
        help_text="Indica el nombre de la bodega")
    es_principal = models.BooleanField(
        default=False, verbose_name = "Es principal",
        help_text="Indica si la bodega corresponde a la bodega principal")
    sucursal =models.ForeignKey(
        Sucursal,
        on_delete=models.SET_NULL,
        null=True,
        related_name='bodegas'
    )
    
    def __str__(self):
        """Representación legible de la bodega incluyendo su estado principal y sucursal."""
        principal_str = " [PRINCIPAL]" if self.es_principal else ""
        sucursal_str = ""

        if self.sucursal:
            sucursal_str = f" - {self.sucursal.nombre_sucursal}"
            if self.sucursal.es_casa_matriz:
                sucursal_str += " (CASA MATRIZ)"
            else:
                sucursal_str = " - Sin sucursal"

        return f"{self.nombre_bodega}{principal_str}{sucursal_str}"
    
    class Meta:
        verbose_name = "Bodega"
        verbose_name_plural = "Bodegas"
        ordering = ['sucursal__nombre_sucursal', '-es_principal', 'nombre_bodega']

# Representa la categoría del productos dentro de la tienda
class Categoria(models.Model):
    """
    Modelo que representa una categoría de productos en el sistema de inventario.
    
    Las categorías permiten organizar jerárquicamente los productos para facilitar
    su gestión y búsqueda. Cada categoría puede tener múltiples productos asociados.

    Attributes:
        nombre_categoria (CharField): Nombre identificatorio único de la categoría.
            - Longitud máxima: 150 caracteres
            - Requerido (null=False, blank=False)
            - Único (unique=True)
        descripcion (CharField): Explicación detallada del alcance de la categoría.
            - Longitud máxima: 150 caracteres
            - Opcional (blank=True)
        created_at (DateTimeField): Marca temporal de creación automática.
            - auto_now_add=True (se establece solo al crear)

    Methods:
        __str__: Representación legible del objeto (devuelve nombre_categoria).

    Meta:
        verbose_name: Nombre singular para la interfaz administrativa.
        verbose_name_plural: Nombre plural para la interfaz administrativa.
    """
    nombre_categoria = models.CharField(
        max_length=150, null=False, blank=False, unique=True,
        help_text="Nombre único de la categoría (ej: 'Guitarras eléctricas')")
    descripcion = models.CharField(
        max_length=150, null=False, blank=True, 
        help_text="Descripción detallada de la categoría")
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Fecha de creación automática al guardar")
    
    def __str__(self):
        return self.nombre_categoria
    
    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['nombre_categoria']

# Representa a los productos asociados a las sucursales y las bodegas, y que se transan en las cajas o puntos de venta
class Producto(models.Model):
    """
    Modelo que representa un producto en el sistema POS.
    
    Attributes:
        sku (str): Código único de identificación del producto (requerido).
        codigo_barra (str): Código de barras del producto (requerido, único).
        categoria_id (ForeignKey): Relación con la categoría a la que pertenece el producto.
        nombre_producto (str): Nombre completo del producto (requerido, único).
        nombre_abreviado (str): Nombre corto para mostrar en tickets/facturas (requerido, único).
        descripcion (str): Detalles adicionales del producto (requerido).
        precio_venta (Decimal): Precio de venta unitario (valores positivos).
        disponible (bool): Disponibilidad del producto.
        imagen (ImageField): Imagen  del producto.
        created_at (date): Fecha de creación del producto.
        update_at (date): Fecha de actualización del producto.
    """
    sku = models.CharField(
        max_length=80, null=False, blank=False, unique=True,
        help_text="Código único de identificación del producto")
    codigo_barra = models.CharField(
        max_length=150, null=False, blank=False, unique=True,
        help_text="Código de barras escaneable")
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    nombre_producto = models.CharField(
        max_length=150, null=False, blank=False, unique=True,
        help_text="Nombre descriptivo del producto")
    nombre_abreviado = models.CharField(
        max_length=80, null=False, blank=False, unique=True,
        help_text="Nombre corto para tickets/facturas")
    descripcion = models.CharField(
        max_length=250, null=False, blank=False,
        help_text="Detalles adicionales del producto")
    precio_venta = models.DecimalField(
        max_digits=12, null=True, blank=True,
        decimal_places=2, validators=[MinValueValidator(0)],
        help_text="Precio unitario en moneda local")
    disponible = models.BooleanField(
        default=True,
        help_text="Disponibilidad del producto")
    imagen = models.ImageField(
        upload_to='files_storage/productos/%Y/%m/%d/',
        null=True, blank=True,
        help_text="Imagen representativa del producto"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Fecha de creación automática al guardar")
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Fecha de actualización automática al modificar")

    def __str__(self):
        return f"{self.nombre_abreviado} | SKU: {self.sku}"
    
    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['categoria__nombre_categoria', 'nombre_producto']  # Orden por categoría y luego alfabético

# Representa el stock disponible en cada bodega
class StockBodega(models.Model):
    """
    Modelo intermedio para gestionar el stock de un producto en una bodega específica.
    
    Attributes:
        producto (ForeignKey): Relación con el producto.
        bodega (ForeignKey): Relación con la bodega.
        stock (PositiveIntegerField): Cantidad disponible en esta bodega.
    """
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    bodega = models.ForeignKey(Bodega, on_delete=models.PROTECT)
    
    stock = models.PositiveIntegerField(
        default=0,
        help_text="Cantidad disponible en esta bodega")
    
    def __str__(self):
        return f"{self.producto.nombre_abreviado} | {self.bodega.nombre_bodega}: {self.stock}"
    
    class Meta:
        verbose_name = "Stock en Bodega"
        verbose_name_plural = "Stocks en Bodegas"
        unique_together = [('producto', 'bodega')]  # Evita duplicados
        
