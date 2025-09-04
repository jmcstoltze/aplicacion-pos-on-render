from django.db import models

from comercio.models import Sucursal
from usuarios.models import Usuario

# Representa a las caja asociadas a cada sucursal y a un usuario
class Caja(models.Model):
    """
    Modelo que representa una caja registradora o punto de venta en una sucursal.

    Cada caja está asociada a una sucursal específica y puede tener un usuario asignado.
    Se utiliza para gestionar transacciones de venta y operaciones de cobro.

    Attributes:
        numero_caja (str): Identificador único o número de la caja (ej: 'CAJ001').
        nombre_caja (str): Nombre descriptivo de la caja (ej: 'Caja Principal').
        estado (bool): Estado operativo (True=Activa, False=Inactiva).
        esta_asignada (bool): Indica si la caja tiene un usuario asignado actualmente.
        usuario_id (Usuario): Usuario asignado a la caja (opcional).
        sucursal_id (Sucursal): Sucursal a la que pertenece la caja (obligatorio).

    Methods:
        __str__: Representación legible que incluye número, nombre y sucursal.
    """
    numero_caja = models.CharField(
        max_length=60, null=False, blank=False,
        verbose_name="Número de caja",
        help_text="Identificador único o número de la caja (ej: 'CAJ001')")
    nombre_caja = models.CharField(
        max_length=80, null=False, blank=False,
        verbose_name="Nombre de la caja",
        help_text="Nombre descriptivo de la caja (ej: 'Caja Principal')")
    estado = models.BooleanField(
        default=False,
        verbose_name="Activa",
        help_text="Indica si la caja está operativa")
    esta_asignada = models.BooleanField(
        default=False,
        verbose_name="Asignada",
        help_text="Indica si la caja tiene un usuario asignado actualmente")
    usuario_id = models.ForeignKey(
        Usuario, on_delete=models.SET_NULL, null=True, blank=True, # Si se elimina el usuario, la relación es NULL
        verbose_name="Usuario asignado",
        help_text="Usuario actualmente asignado a esta caja")
    sucursal_id = models.ForeignKey(
        Sucursal, on_delete=models.PROTECT, # Eliminación protegida
        verbose_name="Sucursal",
        help_text="Sucursal a la que pertenece esta caja")
    
    def __str__(self):
        """
        Representación legible de la caja incluyendo número, nombre y sucursal.
        Ejemplo: "CAJ001 - Caja Principal [Sucursal Centro]"
        """
        estado_str = " (Activa)" if self.estado else " (Inactiva)"
        asignada_str = " - Asignada" if self.esta_asignada else ""
        sucursal_str = f" [{self.sucursal_id.nombre_sucursal}]" if self.sucursal_id else " [Sin sucursal]"
        return f"{self.numero_caja} - {self.nombre_caja}{estado_str}{asignada_str}{sucursal_str}"
    
    class Meta:
        verbose_name = "Caja registradora"
        verbose_name_plural = "Cajas registradoras"
        ordering = ['sucursal_id__nombre_sucursal', 'numero_caja']
