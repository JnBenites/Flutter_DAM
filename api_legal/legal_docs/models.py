from django.db import models
from django.core.validators import MinLengthValidator

class Normativa(models.Model):
    """
    Modelo principal que representa cualquier tipo de normativa (ley, reglamento, código, etc.)
    """
    TIPO_NORMA_CHOICES = [
        ('constitucion', 'Constitución'),
        ('ley', 'Ley'),
        ('codigo', 'Código'),
        ('reglamento', 'Reglamento'),
        ('decreto', 'Decreto'),
        ('acuerdo', 'Acuerdo'),
        ('resolucion', 'Resolución'),
        ('otro', 'Otro'),
    ]
    
    pais = models.CharField(max_length=100, default='Ecuador')
    tipo = models.CharField(max_length=50, choices=TIPO_NORMA_CHOICES)
    nombre = models.CharField(max_length=300)
    nombre_corto = models.CharField(max_length=100, blank=True)
    codigo = models.CharField(max_length=50, blank=True, help_text="Código oficial de la normativa")
    fecha_publicacion = models.DateField()
    fecha_vigencia = models.DateField()
    vigente = models.BooleanField(default=True)
    descripcion = models.TextField(blank=True)
    url_oficial = models.URLField(blank=True)
    ultima_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['tipo', 'nombre']
        verbose_name_plural = "Normativas"
        indexes = [
            models.Index(fields=['tipo']),
            models.Index(fields=['codigo']),
            models.Index(fields=['vigente']),
        ]

    def __str__(self):
        return f"{self.get_tipo_display()} {self.codigo if self.codigo else ''}: {self.nombre}"

class Estructura(models.Model):
    """
    Estructura jerárquica de la normativa (libros, títulos, capítulos, secciones, etc.)
    """
    TIPO_ESTRUCTURA_CHOICES = [
        ('libro', 'Libro'),
        ('titulo', 'Título'),
        ('capitulo', 'Capítulo'),
        ('seccion', 'Sección'),
        ('subseccion', 'Subsección'),
        ('parte', 'Parte'),
        ('division', 'División'),
        ('otro', 'Otra Estructura'),
    ]
    
    normativa = models.ForeignKey(Normativa, on_delete=models.CASCADE, related_name='estructuras')
    tipo = models.CharField(max_length=20, choices=TIPO_ESTRUCTURA_CHOICES)
    numero = models.CharField(max_length=20, blank=True)
    nombre = models.CharField(max_length=300, blank=True)
    padre = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='subestructuras')
    nivel = models.PositiveSmallIntegerField(default=0)
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['normativa', 'nivel', 'orden']
        verbose_name_plural = "Estructuras"

    def __str__(self):
        nombre_display = f" - {self.nombre}" if self.nombre else ""
        return f"{self.get_tipo_display()} {self.numero}{nombre_display}"

class Articulo(models.Model):
    """
    Artículos de la normativa con su contenido principal
    """
    normativa = models.ForeignKey(Normativa, on_delete=models.CASCADE, related_name='articulos')
    estructura = models.ForeignKey(Estructura, null=True, blank=True, on_delete=models.SET_NULL, related_name='articulos')
    numero = models.CharField(max_length=15, validators=[MinLengthValidator(1)])
    contenido = models.TextField()
    orden = models.PositiveIntegerField(default=0)
    notas = models.TextField(blank=True, help_text="Notas o comentarios sobre el artículo")

    class Meta:
        ordering = ['normativa', 'orden']
        unique_together = ['normativa', 'numero']
        verbose_name_plural = "Artículos"

    def __str__(self):
        return f"Art. {self.numero}"

class Inciso(models.Model):
    """
    Incisos dentro de los artículos
    """
    TIPO_INCISO_CHOICES = [
        ('numero', 'Número'),
        ('letra', 'Letra'),
        ('roman', 'Romano'),
        ('item', 'Ítem'),
    ]
    
    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE, related_name='incisos')
    tipo = models.CharField(max_length=10, choices=TIPO_INCISO_CHOICES)
    identificador = models.CharField(max_length=10)
    contenido = models.TextField()
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['articulo', 'orden']
        verbose_name_plural = "Incisos"

    def __str__(self):
        return f"{self.identificador}) {self.contenido[:50]}..."

class Modificacion(models.Model):
    """
    Registro de modificaciones a artículos
    """
    TIPO_MODIFICACION_CHOICES = [
        ('reforma', 'Reforma'),
        ('derogacion', 'Derogación'),
        ('adicion', 'Adición'),
        ('sustitucion', 'Sustitución'),
    ]
    
    normativa = models.ForeignKey(Normativa, on_delete=models.CASCADE, related_name='modificaciones')
    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE, related_name='modificaciones')
    tipo = models.CharField(max_length=20, choices=TIPO_MODIFICACION_CHOICES)
    descripcion = models.TextField()
    fecha = models.DateField()
    normativa_referencia = models.ForeignKey(Normativa, on_delete=models.SET_NULL, null=True, blank=True, 
                                           related_name='modificaciones_realizadas')
    articulo_referencia = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name_plural = "Modificaciones"
        ordering = ['-fecha']

    def __str__(self):
        return f"{self.get_tipo_display()} al Art. {self.articulo.numero}"