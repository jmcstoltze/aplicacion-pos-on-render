from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from .models import Usuario

def obtener_user(username: str) -> User | None:
    """
    Obtiene un usuario del sistema de autenticación mediante su username.

    Esta función busca en la tabla de usuarios de Django (auth_user) por el username
    exacto y retorna el objeto User correspondiente, si existe.

    Args:
        username (str): Nombre de usuario a buscar (case-sensitive).

    Returns:
        User | None: Instancia del modelo User si se encuentra, None si no existe.

    Raises:
        User.DoesNotExist, ValueError, TypeError: múltiples excepciones potenciales.

    Example:
        >>> user = obtener_user('usuario1')
        >>> if user:
        ...     print(f"Usuario encontrado: {user.email}")
    """
    try:
        return User.objects.get(username=username)
    except (User.DoesNotExist, ValueError, TypeError):
        return None
    
def obtener_usuario(user: User) -> Usuario | None:
    """
    Obtiene el usuario extendido (Usuario) asociado a un User de Django.

    Busca en el modelo extendido Usuario (relacionado con OneToOne a User) y retorna
    la instancia correspondiente al User proporcionado.

    Args:
        user (User): Instancia del modelo User de Django al que está asociado el Usuario.

    Returns:
        Usuario | None: Instancia del modelo Usuario si existe, None si no se encuentra.

    Raises:
        Usuario.DoesNotExist, ValueError, TypeError): múltiples excepciones potenciales.

    Example:
        >>> from django.contrib.auth.models import User
        >>> user = User.objects.get(pk=1)
        >>> usuario = obtener_usuario(user)
        >>> if usuario:
        ...     print(f"Perfil extendido: {usuario.telefono}")
    """
    try:
        return Usuario.objects.get(usuario=user)
    except (Usuario.DoesNotExist, ValueError, TypeError):
        return None

def obtener_datos_usuario(user: User) -> dict:
    """
    Obtiene los datos extendidos de un usuario desde el modelo Usuario y los formatea.

    Esta función toma un objeto User de Django, busca su perfil extendido relacionado (Usuario)
    y devuelve un diccionario con los datos formateados para su visualización.

    Parámetros:
        user (User): Instancia del modelo User de Django (auth.User) para la cual se obtendrán
                   los datos extendidos.

    Retorna:
        dict: Diccionario con los datos del usuario formateados con las siguientes claves:
            - 'rol': Nombre del rol (capitalizado, ej. 'Administrador')
            - 'ap_paterno': Apellido paterno (formato título, ej. 'González')
            - 'ap_materno': Apellido materno (formato título, ej. 'Pérez')
            - 'nombres': Nombres (formato título, ej. 'María José')
            - 'username': Nombre de usuario (minúsculas, ej. 'maria.perez')
            - 'email': Correo electrónico (minúsculas, ej. 'maria@ejemplo.com')
            - 'telefono': Número telefónico (sin formato especial)

    Excepciones:
        Usuario.DoesNotExist: Si no existe un perfil Usuario asociado al User.
        AttributeError: Si algún campo esperado no existe en el modelo Usuario.

    Ejemplo:
        >>> usuario = User.objects.get(username='ana.gomez')
        >>> datos = obtener_datos_usuario(usuario)
        >>> print(datos['nombres'])
        'Ana María'
        >>> print(datos['rol'])
        'Jefe de Local'
    """
    try:
        usuario = Usuario.objects.get(usuario=user)

        return {
            'rol': usuario.rol.nombre_rol.capitalize(),
            'ap_paterno': usuario.ap_paterno.title(),
            'ap_materno': usuario.ap_materno.title(),
            'nombres': usuario.nombres.title(),
            'username': user.username.lower(),
            'email': user.email.lower(),
            'telefono': usuario.telefono,
        }
    except (ObjectDoesNotExist, AttributeError):
        return {}