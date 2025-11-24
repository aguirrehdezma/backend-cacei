from django.db import models
from django.conf import settings

# Create your models here.
class Profesor(models.Model):
    """
    Modelo para representar a un Profesor.
    Si el profesor tiene un usuario tipo 'docente', puede acceder al sistema.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='profesor_profile',
        help_text='Usuario asociado si el profesor tiene acceso al sistema como docente'
    )
    numero_empleado = models.CharField(max_length=20, unique=True)
    apellido_paterno = models.CharField(max_length=50)
    apellido_materno = models.CharField(max_length=50)
    nombres = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    nombramiento_actual = models.CharField(max_length=100)
    antiguedad = models.PositiveSmallIntegerField()
    experiencia_ingenieria = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Profesor'
        verbose_name_plural = 'Profesores'
        ordering = ['apellido_paterno', 'apellido_materno', 'nombres']
        
    def __str__(self):
        return f"{self.nombres} {self.apellido_paterno} {self.apellido_materno}"
    
    @property
    def nombre_completo(self):
        return f"{self.nombres} {self.apellido_paterno} {self.apellido_materno}"
    
    @property
    def tiene_acceso_sistema(self):
        # Retorna si el profesor tiene un usuario asociado
        return self.user is not None

class ProgramaEducativo(models.Model):
    ACTIVO = 'activo'
    INACTIVO = 'inactivo'
    EN_REVISION = 'en_revision'

    ESTATUS_CHOICES = [
        (ACTIVO, 'Activo'),
        (INACTIVO, 'Inactivo'),
        (EN_REVISION, 'En Revisión'),
    ]

    clave = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateField(auto_now_add=True)
    estatus = models.CharField(max_length=20, choices=ESTATUS_CHOICES, default=ACTIVO)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

class Curso(models.Model):
    OBLIGATORIO = 'obligatorio'
    OPTATIVO = 'optativo'
    CURRICULAR = 'curricular'

    TIPO_CHOICES = [
        (OBLIGATORIO, 'Obligatorio'),
        (OPTATIVO, 'Optativo'),
        (CURRICULAR, 'Curricular'),
    ]
    
    programa = models.ForeignKey(ProgramaEducativo, on_delete=models.PROTECT)
    
    clave = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    seriacion = models.TextField(blank=True, null=True)
    ubicacion = models.CharField(max_length=50)
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES, default=OBLIGATORIO)
    horas_totales = models.IntegerField()
    objetivo_general = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.clave + " - " + self.nombre

class Institucion(models.Model):
    nombre = models.CharField(max_length=100)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

class Organizacion(models.Model):
    nombre = models.CharField(max_length=100)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

class Periodo(models.Model):
    SEMESTRE_CHOICES = [
        ('EM', 'Enero-Mayo'),
        ('AD', 'Agosto-Diciembre'),
    ]
    
    semestre = models.CharField(max_length=2, choices=SEMESTRE_CHOICES)
    anio = models.PositiveSmallIntegerField()
    nombre = models.CharField(max_length=6, editable=False)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        # Generar nombre automáticamente antes de guardar
        self.nombre = f"{self.semestre}{self.anio}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.nombre
