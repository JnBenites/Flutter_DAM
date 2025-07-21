Legal API Ecuador - Documentación
Descripción General

API REST para la gestión y consulta de normativas legales ecuatorianas. Permite almacenar, organizar y consultar leyes, códigos, reglamentos y otras normativas con su estructura jerárquica completa.

Arquitectura del Sistema
Modelos de Datos
1. Normativa

Modelo principal que representa cualquier tipo de normativa legal.

Campos:

id: Identificador único

tipo: Tipo de normativa (constitución, ley, código, reglamento, decreto, acuerdo, resolución, otro)

nombre: Nombre completo de la normativa

nombre_corto: Nombre abreviado

codigo: Código oficial de la normativa

pais: País de origen (por defecto: Ecuador)

fecha_publicacion: Fecha de publicación oficial

fecha_vigencia: Fecha de entrada en vigencia

vigente: Estado de vigencia (activo/inactivo)

descripcion: Descripción detallada

url_oficial: URL del documento oficial

ultima_actualizacion: Timestamp de última modificación

2. Estructura

Representa la organización jerárquica de las normativas (libros, títulos, capítulos, etc.).

Campos:

id: Identificador único

normativa: Referencia a la normativa padre

tipo: Tipo de estructura (libro, título, capítulo, sección, subsección, parte, división, otro)

numero: Numeración de la estructura

nombre: Nombre descriptivo

padre: Referencia a estructura padre (auto-referencia)

nivel: Nivel jerárquico (0 = raíz)

orden: Orden de aparición

3. Artículo

Contiene los artículos individuales de cada normativa.

Campos:

id: Identificador único

normativa: Referencia a la normativa

estructura: Referencia a la estructura contenedora

numero: Número del artículo

contenido: Texto completo del artículo

orden: Orden de aparición

notas: Comentarios adicionales

4. Inciso

Subdivisiones dentro de los artículos.

Campos:

id: Identificador único

articulo: Referencia al artículo padre

tipo: Tipo de numeración (número, letra, romano, ítem)

identificador: Identificador del inciso (1, a, i, etc.)

contenido: Texto del inciso

orden: Orden de aparición

5. Modificación

Registro histórico de cambios en los artículos.

Campos:

id: Identificador único

normativa: Normativa que contiene el artículo modificado

articulo: Artículo afectado

tipo: Tipo de modificación (reforma, derogación, adición, sustitución)

descripcion: Descripción del cambio

fecha: Fecha de la modificación

normativa_referencia: Normativa que realiza la modificación

articulo_referencia: Artículo de referencia

API Endpoints
Normativas
Listar Normativas
GET /api/normativas/


Parámetros de consulta:

tipo: Filtrar por tipo de normativa

vigente: Filtrar por estado de vigencia

search: Búsqueda por nombre o código

page: Número de página (paginación)

Respuesta:

{
  "count": 150,
  "next": "http://api.example.com/normativas/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "tipo": "codigo",
      "tipo_display": "Código",
      "nombre": "Código Civil",
      "nombre_corto": "CC",
      "codigo": "CC-001",
      "pais": "Ecuador",
      "fecha_publicacion": "2005-06-10",
      "vigente": true,
      "estado": "Vigente"
    }
  ]
}

Obtener Normativa Específica
GET /api/normativas/{id}/


Respuesta: Incluye estructuras y artículos completos.

Crear Normativa
POST /api/normativas/
Content-Type: application/json

{
  "tipo": "ley",
  "nombre": "Ley de Ejemplo",
  "codigo": "LE-001",
  "fecha_publicacion": "2024-01-15",
  "fecha_vigencia": "2024-02-01",
  "vigente": true,
  "descripcion": "Descripción de la ley"
}

Estructuras
Listar Estructuras
GET /api/estructuras/


Parámetros:

normativa: ID de la normativa

tipo: Tipo de estructura

padre: ID de la estructura padre

Crear Estructura
POST /api/estructuras/
Content-Type: application/json

{
  "normativa": 1,
  "tipo": "titulo",
  "numero": "I",
  "nombre": "Disposiciones Generales",
  "padre": null,
  "nivel": 0,
  "orden": 1
}

Artículos
Listar Artículos
GET /api/articulos/


Parámetros:

normativa: ID de la normativa

estructura: ID de la estructura

search: Búsqueda en contenido

Obtener Artículo con Incisos
GET /api/articulos/{id}/


Respuesta:

{
  "id": 1,
  "numero": "1",
  "contenido": "Texto del artículo...",
  "notas": "",
  "orden": 1,
  "normativa": 1,
  "estructura": 1,
  "estructura_nombre": "Disposiciones Generales",
  "estructura_tipo": "Título",
  "incisos": [
    {
      "id": 1,
      "tipo": "numero",
      "identificador": "1",
      "contenido": "Primer inciso...",
      "orden": 1
    }
  ],
  "modificaciones": []
}

Búsqueda Avanzada
Búsqueda Completa
POST /api/busqueda-avanzada/
Content-Type: application/json

{
  "texto": "derechos fundamentales",
  "normativa_tipo": "constitucion",
  "vigente": true,
  "fecha_desde": "2008-01-01",
  "fecha_hasta": "2024-12-31"
}

Configuración del Proyecto
Dependencias (requirements.txt)
django
djangorestframework
djangorestframework-simplejwt
gunicorn
psycopg2-binary
django-cors-headers
django-filter

Configuración Principal (settings.py)

Aplicaciones Instaladas:

Django REST Framework

Django Filters

Aplicación personalizada legal_docs

Configuración REST Framework:

Paginación: 20 elementos por página

Permisos: Acceso público (AllowAny)

Filtros: DjangoFilterBackend, SearchFilter

Base de Datos:

SQLite3 (desarrollo)

Configurado para PostgreSQL en producción

Seguridad:

CSRF_TRUSTED_ORIGINS configurado

DEBUG = False en producción

ALLOWED_HOSTS = ′\*′

URLs del Proyecto

Endpoints principales:

/api/normativas/ - CRUD de normativas

/api/estructuras/ - CRUD de estructuras

/api/articulos/ - CRUD de artículos

/api/incisos/ - CRUD de incisos

/api/modificaciones/ - CRUD de modificaciones

/api/busqueda-avanzada/ - Búsqueda avanzada

Serializers
Características Principales

Serialización Anidada: Los serializers incluyen relaciones completas

Campos Calculados: Campos como tipo_display y estado

Campos de Solo Lectura: Relaciones y campos calculados

Optimización: Serializer específico para listados (NormativaListSerializer)

Ejemplo de Uso
# Serializar una normativa completa
normativa = Normativa.objects.get(id=1)
serializer = NormativaSerializer(normativa)
data = serializer.data

# Crear un nuevo artículo
data = {
    'normativa': 1,
    'numero': '15',
    'contenido': 'Contenido del artículo...',
    'orden': 15
}
serializer = ArticuloSerializer(data=data)
if serializer.is_valid():
    articulo = serializer.save()

Casos de Uso
1. Consulta de Normativa Completa

Obtener una ley con toda su estructura jerárquica, artículos e incisos.

2. Búsqueda por Contenido

Buscar artículos que contengan términos específicos en diferentes normativas.

3. Seguimiento de Modificaciones

Rastrear cambios históricos en artículos específicos.

4. Navegación Jerárquica

Explorar la estructura de una normativa desde libros hasta incisos.

Consideraciones de Rendimiento

Índices de Base de Datos: Configurados en campos frecuentemente consultados

Paginación: Implementada en todos los listados

Campos de Solo Lectura: Evitan consultas innecesarias

Serializers Optimizados: Diferentes serializers para listado y detalle

Despliegue

Configuración de Producción:

Servidor: Gunicorn

Archivos estáticos: Configurados para servir desde /staticfiles/

CORS: Configurado para dominios específicos

Base de datos: PostgreSQL recomendada

Variables de Entorno Recomendadas:

SECRET_KEY: Clave secreta de Django

DATABASE_URL: URL de conexión a base de datos

ALLOWED_HOSTS: Hosts permitidos

DEBUG: False en producción