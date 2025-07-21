from rest_framework import viewsets
from .models import Normativa, Estructura, Articulo, Inciso, Modificacion
from .serializers import (
    NormativaSerializer, EstructuraSerializer, ArticuloSerializer,
    IncisoSerializer, ModificacionSerializer
)

class NormativaViewSet(viewsets.ModelViewSet):
    queryset = Normativa.objects.all()
    serializer_class = NormativaSerializer

class EstructuraViewSet(viewsets.ModelViewSet):
    queryset = Estructura.objects.all()
    serializer_class = EstructuraSerializer

class ArticuloViewSet(viewsets.ModelViewSet):
    queryset = Articulo.objects.all()
    serializer_class = ArticuloSerializer

class IncisoViewSet(viewsets.ModelViewSet):
    queryset = Inciso.objects.all()
    serializer_class = IncisoSerializer

class ModificacionViewSet(viewsets.ModelViewSet):
    queryset = Modificacion.objects.all()
    serializer_class = ModificacionSerializer

from rest_framework.views import APIView
from rest_framework.response import Response

class BusquedaAvanzadaView(APIView):
    def get(self, request):
        # Implementa tu lógica de búsqueda avanzada aquí
        return Response({"message": "Búsqueda avanzada"})