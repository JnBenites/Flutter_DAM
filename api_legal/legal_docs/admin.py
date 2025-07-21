from django.contrib import admin
from django.utils.html import format_html
from .models import Normativa, Estructura, Articulo, Inciso, Modificacion

class IncisoInline(admin.TabularInline):
    model = Inciso
    extra = 0
    fields = ['tipo', 'identificador', 'contenido', 'orden']
    ordering = ['orden']
    classes = ['collapse']

class ModificacionInline(admin.TabularInline):
    model = Modificacion
    extra = 0
    fields = ['tipo', 'fecha', 'descripcion', 'normativa_referencia']
    readonly_fields = ['fecha']
    classes = ['collapse']

class ArticuloAdmin(admin.ModelAdmin):
    list_display = ['numero_compuesto', 'normativa_link', 'estructura_link', 'cantidad_incisos']
    list_filter = ['normativa', 'normativa__tipo', 'normativa__vigente']
    search_fields = ['numero', 'contenido', 'notas']
    inlines = [IncisoInline, ModificacionInline]
    fieldsets = [
        ('Información Básica', {
            'fields': ['normativa', 'estructura', 'numero', 'orden']
        }),
        ('Contenido', {
            'fields': ['contenido', 'notas']
        }),
    ]
    
    def numero_compuesto(self, obj):
        return f"Art. {obj.numero}"
    numero_compuesto.short_description = 'Artículo'
    numero_compuesto.admin_order_field = 'numero'
    
    def normativa_link(self, obj):
        return format_html('<a href="/admin/leyes/normativa/{}/change/">{}</a>',
                          obj.normativa.id, obj.normativa.nombre_corto or obj.normativa.nombre)
    normativa_link.short_description = 'Normativa'
    normativa_link.admin_order_field = 'normativa__nombre'
    
    def estructura_link(self, obj):
        if obj.estructura:
            return format_html('<a href="/admin/leyes/estructura/{}/change/">{}</a>',
                              obj.estructura.id, str(obj.estructura))
        return "-"
    estructura_link.short_description = 'Estructura'
    
    def cantidad_incisos(self, obj):
        return obj.incisos.count()
    cantidad_incisos.short_description = 'Incisos'

class EstructuraInline(admin.TabularInline):
    model = Estructura
    extra = 0
    fields = ['tipo', 'numero', 'nombre', 'nivel', 'padre', 'orden']
    ordering = ['nivel', 'orden']
    classes = ['collapse']

class EstructuraAdmin(admin.ModelAdmin):
    list_display = ['nombre_completo', 'normativa_link', 'tipo', 'nivel', 'cantidad_articulos']
    list_filter = ['normativa', 'tipo', 'nivel']
    search_fields = ['nombre', 'numero']
    inlines = [EstructuraInline]
    fieldsets = [
        ('Información Básica', {
            'fields': ['normativa', 'tipo', 'nombre', 'numero', 'padre']
        }),
        ('Jerarquía', {
            'fields': ['nivel', 'orden']
        }),
    ]
    
    def nombre_completo(self, obj):
        return f"{obj.get_tipo_display()} {obj.numero or ''} - {obj.nombre or ''}".strip(' -')
    nombre_completo.short_description = 'Estructura'
    
    def normativa_link(self, obj):
        return format_html('<a href="/admin/leyes/normativa/{}/change/">{}</a>',
                          obj.normativa.id, obj.normativa.nombre_corto or obj.normativa.nombre)
    normativa_link.short_description = 'Normativa'
    normativa_link.admin_order_field = 'normativa__nombre'
    
    def cantidad_articulos(self, obj):
        return obj.articulos.count()
    cantidad_articulos.short_description = 'Artículos'

class ArticuloInline(admin.TabularInline):
    model = Articulo
    extra = 0
    fields = ['numero', 'contenido_truncado']
    readonly_fields = ['contenido_truncado']
    
    def contenido_truncado(self, obj):
        return (obj.contenido[:50] + '...') if len(obj.contenido) > 50 else obj.contenido
    contenido_truncado.short_description = 'Contenido'

class NormativaAdmin(admin.ModelAdmin):
    list_display = ['nombre_completo', 'tipo', 'pais', 'fecha_publicacion', 'vigente', 'estado_color']
    list_filter = ['tipo', 'vigente', 'pais']
    search_fields = ['nombre', 'nombre_corto', 'codigo', 'descripcion']
    inlines = [ArticuloInline, EstructuraInline]
    fieldsets = [
        ('Información Básica', {
            'fields': ['tipo', 'nombre', 'nombre_corto', 'codigo', 'pais']
        }),
        ('Fechas', {
            'fields': ['fecha_publicacion', 'fecha_vigencia', 'vigente']
        }),
        ('Contenido Adicional', {
            'fields': ['descripcion', 'url_oficial'],
            'classes': ['collapse']
        }),
    ]
    readonly_fields = ['ultima_actualizacion']
    
    def nombre_completo(self, obj):
        return f"{obj.get_tipo_display()} {obj.codigo or ''}: {obj.nombre}".strip()
    nombre_completo.short_description = 'Normativa'
    
    def estado_color(self, obj):
        color = 'green' if obj.vigente else 'red'
        return format_html('<span style="color: {};">{}</span>',
                          color, "Vigente" if obj.vigente else "No vigente")
    estado_color.short_description = 'Estado'
    estado_color.admin_order_field = 'vigente'

class ModificacionAdmin(admin.ModelAdmin):
    list_display = ['tipo', 'articulo_link', 'fecha', 'normativa_link']
    list_filter = ['tipo', 'fecha', 'normativa']
    search_fields = ['descripcion', 'articulo__numero', 'articulo_referencia']
    date_hierarchy = 'fecha'
    
    def articulo_link(self, obj):
        return format_html('<a href="/admin/leyes/articulo/{}/change/">Art. {}</a>',
                          obj.articulo.id, obj.articulo.numero)
    articulo_link.short_description = 'Artículo'
    
    def normativa_link(self, obj):
        return format_html('<a href="/admin/leyes/normativa/{}/change/">{}</a>',
                          obj.normativa.id, obj.normativa.nombre_corto or obj.normativa.nombre)
    normativa_link.short_description = 'Normativa'

admin.site.register(Normativa, NormativaAdmin)
admin.site.register(Estructura, EstructuraAdmin)
admin.site.register(Articulo, ArticuloAdmin)
admin.site.register(Modificacion, ModificacionAdmin)