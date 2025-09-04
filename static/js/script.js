// Función para mostrar/ocultar el menú
function toggleMenu() {
    const sidebar = document.getElementById('sidebar');
    const content = document.getElementById('content');
    sidebar.classList.toggle('active');
    
    // Solo para móviles (≤768px)
    if (window.innerWidth <= 768) {
        content.classList.toggle('sidebar-active');
    } else {
        // Para pantallas grandes (>768px)
        content.classList.toggle('shifted');
    }
}

// Cerrar menú al hacer clic fuera de él (versión corregida)
document.addEventListener('click', function(event) {
    const sidebar = document.getElementById('sidebar');
    const hamburger = document.querySelector('.navbar-toggler-icon');
    const content = document.getElementById('content');
    
    if (!sidebar.contains(event.target) && event.target !== hamburger && !hamburger.contains(event.target)) {
        sidebar.classList.remove('active');
        
        // Elimina ambas clases para asegurar el estado correcto
        content.classList.remove('shifted', 'sidebar-active');
    }
});

// Función para manejar los submenús
document.querySelectorAll('.submenu-toggle').forEach(item => {
    item.addEventListener('click', function(e) {
    e.preventDefault();
    const parent = this.parentElement;
    parent.classList.toggle('active');
            
    // Cerrar otros submenús abiertos
    document.querySelectorAll('.has-submenu').forEach(submenu => {
        if (submenu !== parent && submenu.classList.contains('active')) {
            submenu.classList.remove('active');
        }
    });
});
});

// Función para filtros de categorías
document.getElementById('branchSelect').addEventListener('change', function() {
    
    // Filtrar con AJAX
    fetch(`?categoria=${this.value}`)
        .then(response => response.text())
        .then(html => {
            document.getElementById('productos-container').innerHTML = html;
        });
});

// Función para búsqueda en edición de productos
document.getElementById('searchInput').addEventListener('input', function(e) {
    const searchTerm = e.target.value;
    
    // Cancelar peticiones anteriores si existe
    if (this.searchTimeout) {
        clearTimeout(this.searchTimeout);
    }
    
    // Esperar 300ms después de que el usuario deja de escribir
    this.searchTimeout = setTimeout(() => {
        fetch(`?search=${encodeURIComponent(searchTerm)}&ajax=1`)
            .then(response => response.text())
            .then(html => {
                document.getElementById('productos-container').innerHTML = html;
            });
    }, 300);
});

// Función para habilitar/deshabilitar el modo edición
function enableEditMode() {
    const editButtons = document.querySelectorAll('.edit-buttons');
    editButtons.forEach(button => {
        button.classList.toggle('d-none');
    });
}

// Función para cargar datos del producto en el modal de edición
function loadProductData(id, sku, codigo_barra, categoria_id, nombre_producto, nombre_abreviado, descripcion, precio_venta) {
    // Llenar el formulario con los datos del producto
    document.getElementById('editProductId').value = id;
    document.getElementById('editProductSKU').value = sku;
    document.getElementById('editProductCode').value = codigo_barra;
    document.getElementById('editProductCategory').value = categoria_id;
    document.getElementById('editProductName').value = nombre_producto;
    document.getElementById('editProductAbrName').value = nombre_abreviado;
    document.getElementById('editProductDescp').value = descripcion;
    // document.getElementById('editProductPrice').value = precio_venta;

    // Formatear precio sin decimales
    const precioSinDecimales = parseFloat(precio_venta).toFixed(0);
    document.getElementById('editProductPrice').value = precioSinDecimales;
}

// Manejar envío del formulario de edición
document.getElementById('editProductForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const formData = new FormData(this);
    const submitButton = this.querySelector('button[type="submit"]');
    submitButton.disabled = true;
    submitButton.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Guardando...';
    
    fetch(this.action, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': formData.get('csrfmiddlewaretoken')
        }
    })
    .then(response => {
        if (response.redirected) {
            window.location.href = response.url;
        }
        return response;
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error al actualizar el producto: ' + error.message);
    })
    .finally(() => {
        submitButton.disabled = false;
        submitButton.innerHTML = 'Guardar Cambios';
    });
});

// Manejar envío del formulario de edición
document.getElementById('editProductForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const formData = new FormData(this);
    
    fetch('/edicion_productos/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': formData.get('csrfmiddlewaretoken')
        }
    })
    .then(response => {
        if (response.redirected) {
            window.location.href = response.url;
        } else {
            return response.json();
        }
    })
    .then(data => {
        if (data && data.success) {
            window.location.reload();
        } else if (data) {
            alert(data.message || 'Error al actualizar el producto');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error al actualizar el producto');
    });
});

// Función para filtros de bodegas
document.getElementById('branchSelectBodega').addEventListener('change', function() {

    // Filtrar con AJAX
    fetch(`?bodega=${this.value}`)
        .then(response => response.text())
        .then(html => {
            document.getElementById('productos-container'),this.innerHTML = html;
        })
});

// Función para búsqueda en stock de productos (sin implementar)

// Función para las modificaciones de stock en las bodegas
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('formMasivo').addEventListener('submit', function(e) {
        const bodegaId = document.querySelector('input[name="bodega_id"]').value;
        if(bodegaId === 'all') {
            e.preventDefault();
            alert('Debes seleccionar una bodega específica para hacer ajustes');
            return false;
        }
        
        let hasChanges = false;
        document.querySelectorAll('input[type="number"]').forEach(input => {
            if(input.value !== "0") hasChanges = true;
        });
        
        if(!hasChanges && !(e.submitter && e.submitter.name === 'producto_id')) {
            e.preventDefault();
            alert('No hay cambios para guardar');
            return false;
        }
    });
});

// Cambio automático del año en el footer
document.getElementById('year').textContent = new Date().getFullYear();

// Función para cierre de sesión
document.addEventListener('DOMContentLoaded', function () {
    const logoutLink = document.getElementById('logoutLink');

    logoutLink.addEventListener('click', function (e) {
        e.preventDefault(); // Evita la navegación inmediata

        const confirmLogout = confirm("¿Está seguro de que desea cerrar sesión?");
        if (confirmLogout) {
            // Redirecciona manualmente al logout
            window.location.href = logoutLink.getAttribute('data-logout-url');
        }
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const logoutLink = document.getElementById('logoutLink2');

    logoutLink.addEventListener('click', function (e) {
        e.preventDefault(); // Evita la navegación inmediata

        const confirmLogout = confirm("¿Está seguro de que desea cerrar sesión?");
        if (confirmLogout) {
            // Redirecciona manualmente al logout
            window.location.href = logoutLink.getAttribute('data-logout-url');
        }
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const logoutLink = document.getElementById('logoutLink3');

    logoutLink.addEventListener('click', function (e) {
        e.preventDefault(); // Evita la navegación inmediata

        const confirmLogout = confirm("¿Está seguro de que desea cerrar sesión?");
        if (confirmLogout) {
            // Redirecciona manualmente al logout
            window.location.href = logoutLink.getAttribute('data-logout-url');
        }
    });
});

//////////////// asignar sucursales ////////////////
