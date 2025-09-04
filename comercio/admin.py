from django.contrib import admin
from django.http import HttpResponse
import csv
from .models import Comercio, Sucursal, Bodega, Categoria, Producto, StockBodega

# ==================== COMERCIO ====================
@admin.register(Comercio)
class ComercioAdmin(admin.ModelAdmin):
    list_display = ('nombre_comercio', 'razon_social', 'email', 'telefono_formateado')
    search_fields = ('nombre_comercio', 'razon_social', 'email')
    ordering = ('nombre_comercio',)
    actions = ['export_to_csv']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre_comercio', 'razon_social')
        }),
        ('Contacto', {
            'fields': ('email', 'telefono')
        }),
    )

    def telefono_formateado(self, obj):
        return f"+{obj.telefono[:3]} {obj.telefono[3:]}"
    telefono_formateado.short_description = 'Teléfono'

    def export_to_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="comercios.csv"'
        response.write('\ufeff')  # BOM para UTF-8

        writer = csv.writer(response)
        writer.writerow(['Nombre Comercio', 'Razón Social', 'Email', 'Teléfono'])

        for comercio in queryset:
            writer.writerow([
                comercio.nombre_comercio,
                comercio.razon_social,
                comercio.email,
                f"+{comercio.telefono[:3]} {comercio.telefono[3:]}"
            ])

        return response
    export_to_csv.short_description = "Exportar seleccionados a CSV"

# ==================== SUCURSAL ====================
class SucursalInline(admin.TabularInline):
    model = Sucursal
    extra = 0
    fields = ('nombre_sucursal', 'es_casa_matriz', 'estado')
    readonly_fields = ('es_casa_matriz',)

@admin.register(Sucursal)
class SucursalAdmin(admin.ModelAdmin):
    list_display = ('nombre_sucursal', 'comercio_id', 'comuna', 'es_casa_matriz', 'estado', 'esta_asignada', 'get_jefe_asignado')
    list_filter = ('comercio_id', 'comuna__region', 'es_casa_matriz', 'estado', 'esta_asignada', 'jefe_asignado')
    search_fields = ('nombre_sucursal', 'comercio_id__nombre_comercio', 'direccion', 'jefe_asignado__nombres', 'jefe_asignado__ap_paterno')
    list_editable = ('estado', 'esta_asignada')
    actions = ['export_to_csv']
    raw_id_fields = ['jefe_asignado']  # Para mejor rendimiento con muchos usuarios
    autocomplete_fields = ['jefe_asignado']  # Habilita búsqueda con autocompletado
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre_sucursal', 'comercio_id', 'es_casa_matriz')
        }),
        ('Contacto', {
            'fields': ('email', 'telefono', 'direccion', 'comuna')
        }),
        ('Asignaciones', {
            'fields': ('jefe_asignado', 'estado', 'esta_asignada')
        })
    )

    def get_jefe_asignado(self, obj):
        if obj.jefe_asignado:
            return f"{obj.jefe_asignado.nombres} {obj.jefe_asignado.ap_paterno} ({obj.jefe_asignado.rut})"
        return "No asignado"
    get_jefe_asignado.short_description = 'Jefe Asignado'
    get_jefe_asignado.admin_order_field = 'jefe_asignado'

    def export_to_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="sucursales.csv"'
        response.write('\ufeff')  # BOM para UTF-8

        writer = csv.writer(response)
        writer.writerow([
            'Nombre Sucursal', 'Comercio', 'Casa Matriz', 'Dirección', 
            'Comuna', 'Región', 'Teléfono', 'Email', 'Estado', 'Asignada',
            'Jefe Asignado', 'RUT Jefe', 'Teléfono Jefe'
        ])

        for sucursal in queryset:
            writer.writerow([
                sucursal.nombre_sucursal,
                sucursal.comercio_id.nombre_comercio,
                'Sí' if sucursal.es_casa_matriz else 'No',
                sucursal.direccion,
                sucursal.comuna.nombre_comuna,
                sucursal.comuna.region.nombre_region,
                f"+{sucursal.telefono[:3]} {sucursal.telefono[3:]}",
                sucursal.email,
                'Activa' if sucursal.estado else 'Inactiva',
                'Sí' if sucursal.esta_asignada else 'No',
                f"{sucursal.jefe_asignado.nombres} {sucursal.jefe_asignado.ap_paterno}" if sucursal.jefe_asignado else '',
                sucursal.jefe_asignado.rut if sucursal.jefe_asignado else '',
                sucursal.jefe_asignado.telefono if sucursal.jefe_asignado else ''
            ])

        return response
    export_to_csv.short_description = "Exportar seleccionados a CSV"

# ==================== BODEGA ====================
class BodegaInline(admin.TabularInline):
    model = Bodega
    extra = 0
    fields = ('nombre_bodega', 'es_principal', 'sucursal_id')
    readonly_fields = ('es_principal',)

@admin.register(Bodega)
class BodegaAdmin(admin.ModelAdmin):
    list_display = ('nombre_bodega', 'sucursal_info', 'es_principal', 'comercio_info')
    list_filter = ('es_principal', 'sucursal__comercio', 'sucursal')
    search_fields = ('nombre_bodega', 'sucursal__nombre_sucursal')
    actions = ['export_to_csv']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre_bodega', 'es_principal')
        }),
        ('Ubicación', {
            'fields': ('sucursal',)
        }),
    )

    def sucursal_info(self, obj):
        return obj.sucursal.nombre_sucursal if obj.sucursal else "Sin sucursal"
    sucursal_info.short_description = 'Sucursal'
    sucursal_info.admin_order_field = 'sucursal__nombre_sucursal'

    def comercio_info(self, obj):
        if obj.sucursal and obj.sucursal.comercio_id:
            return obj.sucursal.comercio.nombre_comercio
        return "Sin comercio"
    comercio_info.short_description = 'Comercio'
    comercio_info.admin_order_field = 'sucursal__comercio__nombre_comercio'

    def export_to_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="bodegas.csv"'
        response.write('\ufeff')  # BOM para UTF-8

        writer = csv.writer(response)
        writer.writerow(['Nombre Bodega', 'Principal', 'Sucursal', 'Comercio'])

        for bodega in queryset:
            writer.writerow([
                bodega.nombre_bodega,
                'Sí' if bodega.es_principal else 'No',
                bodega.sucursal.nombre_sucursal if bodega.sucursal else '',
                bodega.sucursal.comercio.nombre_comercio if bodega.sucursal else ''
            ])

        return response
    export_to_csv.short_description = "Exportar seleccionados a CSV"

# ==================== CATEGORÍA ====================
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre_categoria', 'descripcion', 'created_at')
    search_fields = ('nombre_categoria', 'descripcion')
    list_filter = ('created_at',)
    ordering = ('nombre_categoria',)
    actions = ['export_to_csv']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre_categoria', 'descripcion')
        }),
    )

    def export_to_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="categorias.csv"'
        response.write('\ufeff')  # BOM para UTF-8

        writer = csv.writer(response)
        writer.writerow(['Nombre Categoría', 'Descripción', 'Fecha Creación'])

        for categoria in queryset:
            writer.writerow([
                categoria.nombre_categoria,
                categoria.descripcion,
                categoria.created_at.strftime("%d/%m/%Y %H:%M")
            ])

        return response
    export_to_csv.short_description = "Exportar seleccionados a CSV"

# ==================== PRODUCTO ====================
class StockBodegaInline(admin.TabularInline):
    model = StockBodega
    extra = 1
    fields = ('bodega', 'stock')
    verbose_name_plural = 'Stock por Bodega'

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre_abreviado', 'sku', 'precio_venta_formateado', 'disponible', 'stock_total')
    list_filter = ('disponible', 'created_at')
    search_fields = ('nombre_producto', 'nombre_abreviado', 'sku', 'codigo_barra')
    list_editable = ('disponible',)
    ordering = ('nombre_producto',)
    inlines = [StockBodegaInline]
    actions = ['export_to_csv']
    
    fieldsets = (
        ('Identificación', {
            'fields': ('sku', 'codigo_barra')
        }),
        ('Información del Producto', {
            'fields': ('nombre_producto', 'nombre_abreviado', 'descripcion')
        }),
        ('Precio y Disponibilidad', {
            'fields': ('precio_venta', 'disponible')
        }),
        ('Imagen', {
            'fields': ('imagen',)
        }),
    )

    def precio_venta_formateado(self, obj):
        return f"${obj.precio_venta:,.2f}" if obj.precio_venta else "-"
    precio_venta_formateado.short_description = 'Precio'
    precio_venta_formateado.admin_order_field = 'precio_venta'

    def stock_total(self, obj):
        return sum(stock.stock for stock in obj.stockbodega_set.all())
    stock_total.short_description = 'Stock Total'

    def export_to_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="productos.csv"'
        response.write('\ufeff')  # BOM para UTF-8

        writer = csv.writer(response)
        writer.writerow([
            'SKU', 'Código Barras', 'Nombre Producto', 'Nombre Corto', 
            'Descripción', 'Precio', 'Disponible', 'Stock Total'
        ])

        for producto in queryset:
            writer.writerow([
                producto.sku,
                producto.codigo_barra,
                producto.nombre_producto,
                producto.nombre_abreviado,
                producto.descripcion,
                f"${producto.precio_venta:,.2f}" if producto.precio_venta else "",
                'Sí' if producto.disponible else 'No',
                sum(stock.stock for stock in producto.stockbodega_set.all())
            ])

        return response
    export_to_csv.short_description = "Exportar seleccionados a CSV"

# ==================== STOCK BODEGA ====================
@admin.register(StockBodega)
class StockBodegaAdmin(admin.ModelAdmin):
    list_display = ('producto_info', 'bodega_info', 'stock', 'comercio_info')
    list_filter = ('bodega__sucursal__comercio', 'bodega')
    search_fields = ('producto__nombre_producto', 'producto__sku', 'bodega__nombre_bodega')
    list_editable = ('stock',)
    actions = ['export_to_csv']
    list_select_related = ('producto', 'bodega__sucursal__comercio')
    
    def producto_info(self, obj):
        return f"{obj.producto.nombre_abreviado} (SKU: {obj.producto.sku})"
    producto_info.short_description = 'Producto'
    producto_info.admin_order_field = 'producto__nombre_abreviado'

    def bodega_info(self, obj):
        return obj.bodega.nombre_bodega
    bodega_info.short_description = 'Bodega'
    bodega_info.admin_order_field = 'bodega__nombre_bodega'

    def comercio_info(self, obj):
        try:
            if obj.bodega.sucursal and obj.bodega.sucursal.comercio:
                return obj.bodega.sucursal.comercio.nombre_comercio
        except AttributeError:
            pass
        return "Sin comercio"
    comercio_info.short_description = 'Comercio'
    comercio_info.admin_order_field = 'bodega__sucursal__comercio__nombre_comercio'

    def export_to_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="stock_bodegas.csv"'
        response.write('\ufeff')  # BOM para UTF-8

        writer = csv.writer(response)
        writer.writerow(['Producto', 'SKU', 'Bodega', 'Sucursal', 'Comercio', 'Stock'])

        for stock in queryset:

            # Manejo seguro de relaciones
            sucursal_nombre = ''
            comercio_nombre = ''

            try:
                if stock.bodega.sucursal:
                    sucursal_nombre = stock.bodega.sucursal.nombre_sucursal
                    if stock.bodega.sucursal.comercio:
                        comercio_nombre = stock.bodega.sucursal.comercio.nombre_comercio
            except AttributeError:
                pass

            writer.writerow([
                stock.producto.nombre_producto,
                stock.producto.sku,
                stock.bodega.nombre_bodega,
                sucursal_nombre,
                comercio_nombre,
                stock.stock
            ])

        return response
    export_to_csv.short_description = "Exportar seleccionados a CSV"