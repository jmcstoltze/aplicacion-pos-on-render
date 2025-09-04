from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .services import (
    obtener_user,
    obtener_usuario,
    obtener_datos_usuario
)
    
def inicio_sesion(request) -> HttpResponse | HttpResponseRedirect:
    """
    Maneja el proceso de autenticación y redirección de usuarios según su rol.
    
    Esta vista procesa el formulario de inicio de sesión, autentica al usuario
    y lo redirige a la interfaz correspondiente según su rol en el sistema:
    - Superusuario: Panel de administración de Django (/admin/)
    - Administradores: Dashboard de administrador
    - Jefes de Local: Dashboard de jefe de local
    - Cajeros: Dashboard de cajero

    Args:
        request (HttpRequest): Objeto de solicitud HTTP que contiene los datos del formulario.

    Returns:
        HttpResponseRedirect: Redirección al dashboard correspondiente si la autenticación es exitosa.
        HttpResponse: Renderizado de la plantilla de inicio de sesión con mensajes de error si falla.

    Raises:
        PermissionDenied: Si el usuario autenticado no tiene un rol válido asignado.

    Example:
        >>> # Acceso vía POST con credenciales válidas
        >>> response = client.post('/login/', {'username': 'admin', 'password': 'secret'})
        >>> response.status_code
        302  # Redirección (HttpResponseRedirect)
        >>> # Acceso vía GET
        >>> response = client.get('/login/')
        >>> response.status_code
        200  # HttpResponse
    """

    if request.method == 'POST':
        # Obtiene los datos POST del formulario
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = obtener_user(username) # Obtiene el usuario Auth_User

        # Si el usuario no existe lo indica
        if not user:
            return render(request, 'registration/login.html', {'error_message': 'Usuario no existe'})
        
        # Autentica al usuario y contraseña
        auth_user = authenticate(request, username=username, password=password)

        # Si usuario existe lo logea
        if auth_user is not None:
            login(request, auth_user)

            # Verifica si usuario logeado es superusuario
            if auth_user.is_superuser:
                # Redirige a panel de administración de Django
                return redirect('/admin/')

            usuario = obtener_usuario(auth_user) # Obtiene el Usuario

            # Redirección según rol de usuario
            if usuario.rol.nombre_rol in ['Administrador', 'Jefe de local', 'Cajero']:
                return redirect('dashboard')
            else:
                # Manejo de roles no reconocidos
                logout(request)
                return render(request, 'registration/login.html', {'error_message': 'Rol de usuario no válido'})
        else:
            # Credenciales inválidas
            return render(request, 'registration/login.html', {'error_message': 'Credenciales inválidas'})
    else:
        # Método GET muestra el formulario
        return render(request, "registration/login.html", {}) # Renderiza la página

@login_required
def dashboard(request) -> HttpResponse:
    """
    Vista del panel de control para usuarios con rol de Administrador, Jefe de local o Cajero.
    
    Esta vista autenticada muestra el dashboard principal para usuarios del sistema,
    incluyendo los datos del usuario logueado y controles administrativos. Requiere que el
    usuario esté autenticado (gracias al decorador @login_required) y típicamente debería
    verificar también el rol de administrador.

    Args:
        request (HttpRequest): Objeto de solicitud HTTP que contiene los datos de sesión y
                             el objeto User autenticado (disponible en request.user).

    Returns:
        HttpResponse: Renderiza la plantilla 'dashboard-administrador.html' con un contexto
                     que incluye:
                     - datos_usuario (dict): Diccionario estructurado con los datos del
                       usuario obtenidos mediante obtener_datos_usuario().

    Raises:
        PermissionDenied: Si el usuario no tiene los permisos requeridos (manejado por
                        el decorador @login_required).

    Example:
        >>> # Acceso a la vista como usuario autenticado
        >>> response = client.get(reverse('dashboard'))
        >>> response.status_code
        200
        >>> # Acceso no autenticado redirige a login
        >>> client.logout()
        >>> response = client.get(reverse('dashboard'))
        >>> response.status_code
        302
    """
    
    # Rescata datos del Usuario para mostrar en la vista
    datos_usuario = obtener_datos_usuario(request.user)
    return render(request, 'usuarios/views/dashboard.html', {'datos_usuario': datos_usuario})

@login_required    
def cerrar_sesion(request):
    """
    Cierra la sesión del usuario actual y redirige a la página de login.
    
    Args:
        request: Objeto HttpRequest con los datos de la solicitud
        
    Returns:
        HttpResponseRedirect: Redirección a la página de login
        
    Funcionalidades:
        - Cierra la sesión del usuario
        - Limpia la sesión
        - Redirige a la página de login
    """
    logout(request)

    return redirect('inicio_sesion')
