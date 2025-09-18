from django.db import models

# Create your models here.
class ProgramaEducativo(models.Model):
    ACTIVO = 'activo'
    INACTIVO = 'inactivo'
    EN_REVISION = 'en_revision'

    ESTATUS_CHOICES = [
        (ACTIVO, 'Activo'),
        (INACTIVO, 'Inactivo'),
        (EN_REVISION, 'En Revisión'),
    ]

    programa_id = models.AutoField(primary_key=True)
    clave = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateField(auto_now_add=True)
    estatus = models.CharField(max_length=20, choices=ESTATUS_CHOICES, default=ACTIVO)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

class UnidadTematica(models.Model):
    unidad_id = models.AutoField(primary_key=True)
    # Relación con curso_id
    numero = models.IntegerField(unique=True)
    descripcion = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.numero)

class CriterioDesempeno(models.Model):
    criterio_id = models.AutoField(primary_key=True)
    # Relación con atributo_pe_id
    codigo = models.CharField(max_length=10, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.codigo

class Curso(models.Model):
    OBLIGATORIO = 'obligatorio'
    OPTATIVO = 'optativo'

    TIPO_CHOICES = [
        (OBLIGATORIO, 'Obligatorio'),
        (OPTATIVO, 'Optativo'),
    ]
    
    curso_id = models.AutoField(primary_key=True)
    # programa = models.ForeignKey(ProgramaEducativo, on_delete=models.CASCADE, related_name='cursos', db_column='programa_id')
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
        return self.nombre

class EstrategiaEnsenanza(models.Model):
    estrategia_id = models.AutoField(primary_key=True)
    # curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='estrategias_ensenanza', db_column='curso_id')
    numero = models.IntegerField()
    descripcion = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.numero)

class EstrategiaEvaluacion(models.Model):
    estrategia_id = models.AutoField(primary_key=True)
    # curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='estrategias_evaluacion', db_column='curso_id')
    numero = models.IntegerField()
    descripcion = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.numero)

class ObjetivoEducacional(models.Model):
    objetivo_id = models.AutoField(primary_key=True)
    # programa = models.ForeignKey(ProgramaEducativo, on_delete=models.CASCADE, related_name='objetivos_educacionales', db_column='programa_id')
    codigo = models.CharField(max_length=10, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.codigo

class Bibliografia(models.Model):
    bibliografia_id = models.AutoField(primary_key=True)
    # curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='bibliografias', db_column='curso_id')
    numero = models.IntegerField()
    autor = models.CharField(max_length=100)
    titulo = models.CharField(max_length=200)
    editorial = models.CharField(max_length=100)
    anio_publicacion = models.PositiveSmallIntegerField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.numero}. {self.autor} - {self.titulo} ({self.anio_publicacion})"
