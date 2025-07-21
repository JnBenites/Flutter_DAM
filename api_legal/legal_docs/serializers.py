from rest_framework import serializers
from .models import Normativa, Estructura, Articulo, Inciso, Modificacion

class IncisoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inciso
        fields = ['id', 'tipo', 'identificador', 'contenido', 'orden']
        read_only_fields = ['id']

class ModificacionSerializer(serializers.ModelSerializer):
    normativa_referencia_nombre = serializers.CharField(source='normativa_referencia.nombre', read_only=True)
    
    class Meta:
        model = Modificacion
        fields = [
            'id', 'tipo', 'descripcion', 'fecha', 
            'normativa_referencia', 'normativa_referencia_nombre',
            'articulo_referencia'
        ]
        read_only_fields = ['id']

class ArticuloSerializer(serializers.ModelSerializer):
    incisos = IncisoSerializer(many=True, read_only=True)
    modificaciones = ModificacionSerializer(many=True, read_only=True)
    estructura_nombre = serializers.CharField(source='estructura.nombre', read_only=True)
    estructura_tipo = serializers.CharField(source='estructura.get_tipo_display', read_only=True)
    
    class Meta:
        model = Articulo
        fields = [
            'id', 'numero', 'contenido', 'notas', 'orden',
            'normativa', 'estructura', 'estructura_nombre', 'estructura_tipo',
            'incisos', 'modificaciones'
        ]
        read_only_fields = ['id', 'incisos', 'modificaciones']

class EstructuraSerializer(serializers.ModelSerializer):
    subestructuras = serializers.SerializerMethodField()
    articulos = ArticuloSerializer(many=True, read_only=True)
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    
    class Meta:
        model = Estructura
        fields = [
            'id', 'tipo', 'tipo_display', 'numero', 'nombre',
            'padre', 'nivel', 'orden', 'normativa',
            'subestructuras', 'articulos'
        ]
        read_only_fields = ['id', 'subestructuras', 'articulos']

    def get_subestructuras(self, obj):
        return EstructuraSerializer(obj.subestructuras.all(), many=True).data

class NormativaSerializer(serializers.ModelSerializer):
    estructuras = EstructuraSerializer(many=True, read_only=True)
    articulos = ArticuloSerializer(many=True, read_only=True)
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    estado = serializers.CharField(source='get_vigente_display', read_only=True)
    
    class Meta:
        model = Normativa
        fields = [
            'id', 'tipo', 'tipo_display', 'nombre', 'nombre_corto',
            'codigo', 'pais', 'fecha_publicacion', 'fecha_vigencia',
            'vigente', 'estado', 'descripcion', 'url_oficial',
            'ultima_actualizacion', 'estructuras', 'articulos'
        ]
        read_only_fields = ['id', 'ultima_actualizacion', 'estructuras', 'articulos']

class NormativaListSerializer(serializers.ModelSerializer):
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    estado = serializers.CharField(source='get_vigente_display', read_only=True)
    
    class Meta:
        model = Normativa
        fields = [
            'id', 'tipo', 'tipo_display', 'nombre', 'nombre_corto',
            'codigo', 'pais', 'fecha_publicacion', 'vigente', 'estado'
        ]
        read_only_fields = fields