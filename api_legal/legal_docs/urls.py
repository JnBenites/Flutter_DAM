from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    NormativaViewSet,
    EstructuraViewSet,
    ArticuloViewSet,
    IncisoViewSet,
    ModificacionViewSet,
    BusquedaAvanzadaView
)

router = DefaultRouter()
router.register(r'normativas', NormativaViewSet)
router.register(r'estructuras', EstructuraViewSet)
router.register(r'articulos', ArticuloViewSet)
router.register(r'incisos', IncisoViewSet)
router.register(r'modificaciones', ModificacionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('busqueda-avanzada/', BusquedaAvanzadaView.as_view(), name='busqueda-avanzada'),
]