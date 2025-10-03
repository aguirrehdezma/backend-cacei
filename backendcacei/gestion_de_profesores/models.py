from django.db import models

# Create your models here.
class ProfesorCurso(models.Model):
    RESPONSABLE = 'responsable'
    INSTRUCTOR = 'instructor'

    TIPO_CHOICES = [
        (RESPONSABLE, 'Responsable'),
        (INSTRUCTOR, 'Instructor'),
    ]

    profesor_curso_id = models.AutoField(primary_key=True)
    profesor_id = models.ForeignKey('core.Profesor', on_delete=models.PROTECT, related_name='profesores_cursos', db_column='profesor_id')
    curso_id = models.ForeignKey('core.Curso', on_delete=models.PROTECT, related_name='profesores_cursos', db_column='curso_id')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default=RESPONSABLE)
    periodo = models.CharField(max_length=50)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profesor {self.profesor_id} imparte el curso {self.curso_id}"

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

    formacion_id = models.AutoField(primary_key=True)
    profesor_id = models.ForeignKey('core.Profesor', on_delete=models.PROTECT, related_name='formacion_academica', db_column='profesor_id')
    nivel = models.CharField(max_length=20, choices=NIVEL_CHOICES, default=LICENCIATURA)
    institucion = models.CharField(max_length=100)
    pais = models.CharField(max_length=50)
    anio_obtencion = models.PositiveSmallIntegerField()
    cedula_profesional= models.CharField(max_length=50, blank=True, null=True)
    especialidad= models.CharField(max_length=100, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profesor {self.profesor_id} tiene formacion academica de {self.nivel}"

class ExperienciaProfesional(models.Model):
    experiencia_id = models.AutoField(primary_key=True)
    profesor_id = models.ForeignKey('core.Profesor', on_delete=models.PROTECT, related_name='experiencia_profesional', db_column='profesor_id')
    organizacion = models.CharField(max_length=100)
    puesto = models.CharField(max_length=100)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    actividades = models.TextField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profesor {self.profesor_id} trabajó en {self.organizacion} como {self.puesto}"

class ExperienciaDiseno(models.Model):
    diseno_id = models.AutoField(primary_key=True)
    profesor_id = models.ForeignKey('core.Profesor', on_delete=models.PROTECT, related_name='experiencia_disenio', db_column='profesor_id')
    organizacion = models.CharField(max_length=100)
    periodo = models.CharField(max_length=50)
    nivel_experiencia = models.CharField(max_length=50)
    descripcion = models.TextField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profesor {self.profesor_id} tiene experiencia de diseño de {self.nivel_experiencia} en {self.organizacion}"

class LogroProfesional(models.Model):
    logro_id = models.AutoField(primary_key=True)
    profesor_id = models.ForeignKey('core.Profesor', on_delete=models.PROTECT, related_name='logros_profesionales', db_column='profesor_id')
    descripcion = models.TextField()
    anio = models.PositiveSmallIntegerField(null=True, blank=True)
    relevancia = models.TextField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profesor {self.profesor_id} tiene logros de {self.descripcion} en {self.anio}"

class PremioDistincion(models.Model):
    premio_id = models.AutoField(primary_key=True)
    profesor_id = models.ForeignKey('core.Profesor', on_delete=models.PROTECT, related_name='premios_distinciones', db_column='profesor_id')
    descripcion = models.TextField()
    anio = models.PositiveSmallIntegerField(null=True, blank=True)
    institucion_otorga = models.CharField(max_length=100, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profesor {self.profesor_id} recibió el premio {self.descripcion} en {self.anio}"

class ParticipacionOrganizaciones(models.Model):
    participacion_id = models.AutoField(primary_key=True)
    profesor_id = models.ForeignKey('core.Profesor', on_delete=models.PROTECT, related_name='participaciones_organizaciones', db_column='profesor_id')
    organizacion = models.CharField(max_length=100)
    periodo = models.CharField(max_length=50)
    nivel_participacion = models.CharField(max_length=50)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profesor {self.profesor_id} participó en {self.organizacion}"

class CapacitacionDocente(models.Model):
    capacitacion_id = models.AutoField(primary_key=True)
    profesor_id = models.ForeignKey('core.Profesor', on_delete=models.PROTECT, related_name='capacitacion_docente', db_column='profesor_id')
    nombre_curso = models.CharField(max_length=100)
    institucion = models.CharField(max_length=100)
    pais = models.CharField(max_length=50)
    anio_obtencion = models.PositiveSmallIntegerField()
    horas = models.PositiveSmallIntegerField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profesor {self.profesor_id} recibió esta capacitación docente {self.capacitacion_id}"

class ActualizacionDisciplinar(models.Model):
    actualizacion_id = models.AutoField(primary_key=True)
    profesor_id = models.ForeignKey('core.Profesor', on_delete=models.PROTECT, related_name='actualizacion_disciplinar', db_column='profesor_id')
    nombre_curso = models.CharField(max_length=100)
    institucion = models.CharField(max_length=100)
    pais = models.CharField(max_length=50)
    anio_obtencion = models.PositiveSmallIntegerField()
    horas = models.PositiveSmallIntegerField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profesor {self.profesor_id} recibió esta actualización disciplinar {self.actualizacion_id}"

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
    
    producto_id = models.AutoField(primary_key=True)
    profesor_id = models.ForeignKey('core.Profesor', on_delete=models.PROTECT, related_name='productos_academicos', db_column='profesor_id')
    descripcion = models.TextField()
    anio = models.PositiveSmallIntegerField()
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default=PUBLICACION)
    detalles = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Producto académico: {self.descripcion} ({self.tipo})"
