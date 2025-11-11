from django.db import models

# Create your models here.
class ProfesorCurso(models.Model):
    RESPONSABLE = 'responsable'
    INSTRUCTOR = 'instructor'

    TIPO_CHOICES = [
        (RESPONSABLE, 'Responsable'),
        (INSTRUCTOR, 'Instructor'),
    ]

    profesor = models.ForeignKey('core.Profesor', on_delete=models.PROTECT)
    curso = models.ForeignKey('core.Curso', on_delete=models.PROTECT)
    
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default=RESPONSABLE)
    periodo = models.CharField(max_length=50)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profesor {self.profesor.nombres} {self.profesor.apellidos} imparte el curso {self.curso.clave}"

class FormacionAcademica(models.Model):
    LICENCIATURA = 'licenciatura'
    ESPECIALIDAD = 'especialidad'
    MAESTRIA = 'maestria'
    DOCTORADO = 'doctorado'

    NIVEL_CHOICES = [
        (LICENCIATURA, 'Licenciatura'),
        (ESPECIALIDAD, 'Especialidad'),
        (MAESTRIA, 'Maestría'),
        (DOCTORADO, 'Doctorado'),
    ]

    profesor = models.ForeignKey('core.Profesor', on_delete=models.PROTECT)
    institucion = models.ForeignKey('core.Institucion', on_delete=models.PROTECT)
    
    nivel = models.CharField(max_length=20, choices=NIVEL_CHOICES, default=LICENCIATURA)
    pais = models.CharField(max_length=50)
    anio_obtencion = models.PositiveSmallIntegerField()
    cedula_profesional= models.CharField(max_length=50, blank=True, null=True)
    especialidad= models.CharField(max_length=100, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profesor {self.profesor.nombres} {self.profesor.apellidos} tiene formacion academica de {self.nivel}"

class ExperienciaProfesional(models.Model):
    profesor = models.ForeignKey('core.Profesor', on_delete=models.PROTECT)
    organizacion = models.ForeignKey('core.Organizacion', on_delete=models.PROTECT)
    
    puesto = models.CharField(max_length=100)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    actividades = models.TextField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profesor {self.profesor.nombres} {self.profesor.apellidos} trabajó en {self.organizacion.nombre} como {self.puesto}"
    
class ExperienciaDiseno(models.Model):
    profesor = models.ForeignKey('core.Profesor', on_delete=models.PROTECT)
    organizacion = models.ForeignKey('core.Organizacion', on_delete=models.PROTECT)
    
    periodo = models.CharField(max_length=50)
    nivel_experiencia = models.CharField(max_length=50)
    descripcion = models.TextField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profesor {self.profesor.nombres} {self.profesor.apellidos} tiene experiencia de diseño de {self.nivel_experiencia} en {self.organizacion.nombre}"

class LogroProfesional(models.Model):
    profesor = models.ForeignKey('core.Profesor', on_delete=models.PROTECT)
    
    descripcion = models.TextField()
    anio = models.PositiveSmallIntegerField(null=True, blank=True)
    relevancia = models.TextField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profesor {self.profesor.nombres} {self.profesor.apellidos} tiene logros de {self.descripcion} en {self.anio}"

class PremioDistincion(models.Model):
    profesor = models.ForeignKey('core.Profesor', on_delete=models.PROTECT)
    institucion_otorga = models.ForeignKey('core.Organizacion', on_delete=models.PROTECT)
    
    descripcion = models.TextField()
    anio = models.PositiveSmallIntegerField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profesor {self.profesor.nombres} {self.profesor.apellidos} recibió el premio {self.descripcion} en {self.anio}"

class ParticipacionOrganizaciones(models.Model):
    profesor = models.ForeignKey('core.Profesor', on_delete=models.PROTECT)
    organizacion = models.ForeignKey('core.Organizacion', on_delete=models.PROTECT)
    
    periodo = models.CharField(max_length=50)
    nivel_participacion = models.CharField(max_length=50)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profesor {self.profesor.nombres} {self.profesor.apellidos} participó en {self.organizacion.nombre}"

class CapacitacionDocente(models.Model):
    profesor = models.ForeignKey('core.Profesor', on_delete=models.PROTECT)
    institucion = models.ForeignKey('core.Institucion', on_delete=models.PROTECT)
    
    nombre_curso = models.CharField(max_length=100)
    pais = models.CharField(max_length=50)
    anio_obtencion = models.PositiveSmallIntegerField()
    horas = models.PositiveSmallIntegerField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profesor {self.profesor.nombres} {self.profesor.apellidos} recibió esta capacitación docente {self.nombre_curso}"

class ActualizacionDisciplinar(models.Model):
    profesor = models.ForeignKey('core.Profesor', on_delete=models.PROTECT)
    institucion = models.ForeignKey('core.Institucion', on_delete=models.PROTECT)
    
    nombre_curso = models.CharField(max_length=100)
    pais = models.CharField(max_length=50)
    anio_obtencion = models.PositiveSmallIntegerField()
    horas = models.PositiveSmallIntegerField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profesor {self.profesor.nombres} {self.profesor.apellidos} recibió esta actualización disciplinar {self.nombre_curso}"

class ProductoAcademico(models.Model):
    PUBLICACION = 'publicacion'
    PROYECTO = 'proyecto'
    PATENTE = 'patente'
    OTRO = 'otro'

    TIPO_CHOICES = [
        (PUBLICACION, 'Publicación'),
        (PROYECTO, 'Proyecto'),
        (PATENTE, 'Patente'),
        (OTRO, 'Otro'),
    ]
    
    profesor = models.ForeignKey('core.Profesor', on_delete=models.PROTECT)

    descripcion = models.TextField()
    anio = models.PositiveSmallIntegerField()
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default=PUBLICACION)
    detalles = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Producto académico: {self.descripcion} ({self.tipo})"
