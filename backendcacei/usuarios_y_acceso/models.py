from django.db import models

# Create your models here.

class Profesores():
    TIEMPO_COMPLETO = 'tiempo_completo'
    ASIGNATURA = 'asignatura'
    MEDIO_TIEMPO = 'medio_tiempo'
    OTRO = 'otro'

    NOMBRAMIENTO_CHOICES = [
        (TIEMPO_COMPLETO, 'Tiempo Completo'),
        (ASIGNATURA, 'Asignatura'),
        (MEDIO_TIEMPO, 'Medio Tiempo'),
        (OTRO, 'Otro'),
    ]

    profesor_id = models.AutoField(primary_key=True)
    numero_empleado = models.IntegerField()
    apellido_paterno = models.TextField()
    apellido_materno = models.TextField()
    nombres = models.TextField()
    fecha_nacimiento = models.DateField()
    nombramiento_actual = models.CharField(max_length=20, choices=NOMBRAMIENTO_CHOICES, default=TIEMPO_COMPLETO)
    antiguedad = models.IntegerField()
    experiencia_ingenieria = models.BooleanField()
    created_at = models.DateField()
    updated_at = models.DateField()

    def __str__(self):
        return f"Profesor(x) {self.nombres} - {self.apellido_paterno} - {self.apellido_materno}"


class ProfesoresCursos():
    TEORICO = 1
    PRACTICO = 2
    LABORATORIO = 3
    OTRO = 4

    TIPO_CHOICES = [
        (TEORICO, 'Teórico'),
        (PRACTICO, 'Práctico'),
        (LABORATORIO, 'Laboratorio'),
        (OTRO, 'Otro'),
    ]

    profesor_curso_id = models.AutoField(primary_key=True)
    profesor_id = models.ForeignKey(Profesores, on_delete=models.CASCADE, related_name='profesoresCursos', db_column='profesor_id')
    curso_id = models.IntegerField()
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default=TEORICO)
    periodo = models.IntegerField()
    created_at = models.DateField()
    updated_at = models.DateField()

    def __str__(self):
        return f"Profesor(x) {self.profesor_id} imparte el curso de de {self.curso_id}"


class FormacionAcademica():
    LICENCIATURA = 1
    MAESTRIA = 2
    DOCTORADO = 3
    OTRO = 4

    NIVEL_CHOICES = [
        (LICENCIATURA, 'Licenciatura'),
        (MAESTRIA, 'Maestría'),
        (DOCTORADO, 'Doctorado'),
        (OTRO, 'Otro'),
    ]

    formacion_id = models.AutoField(primary_key=True)
    profesor_id = models.IntegerField(Profesores, on_delete=models.CASCADE, related_name='formacionAcademica', db_column='profesor_id')
    nivel = models.PositiveSmallIntegerField(choices=NIVEL_CHOICES, default=LICENCIATURA)
    institucion = models.TextField()
    pais = models.TextField()
    anno_obtencion = models.DateField()
    cedula_profesional= models.TextField()
    especialidad= models.TextField()
    created_at = models.DateField()
    updated_at = models.DateField()

    def __str__(self):
        return f"Profesor(x) {self.profesor_id} tiene formacion academica de {self.nivel}"


class ExperienciaProfesional():
    DOCENTE = 1
    DIRECTIVO = 2
    INVESTIGADOR = 3
    CONSULTOR = 4
    OTRO = 5

    PUESTO_CHOICES = [
        (DOCENTE, 'Docente'),
        (DIRECTIVO, 'Directivo'),
        (INVESTIGADOR, 'Investigador'),
        (CONSULTOR, 'Consultor'),
        (OTRO, 'Otro'),
    ]

    experiencia_id = models.AutoField(primary_key=True)
    profesor_id = models.IntegerField(Profesores, on_delete=models.CASCADE, related_name='experienciaProfesional', db_column='profesor_id')
    organización = models.TextField()
    puesto = models.CharField(max_length=20, choices=PUESTO_CHOICES, default=DOCENTE)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    actividades = models.TextField()
    created_at = models.DateField()
    updated_at = models.DateField()

    def __str__(self):
        return f"Profesor(x) {self.profesor_id} tiene experiencia orifesional de {self.experiencia_id}"
    

class ExperienciaDiseno():
    BASICO = 1
    INTERMEDIO = 2
    AVANZADO = 3
    OTRO = 4

    NIVEL_EXPERIENCIA_CHOICES = [
        (BASICO, 'Básico'),
        (INTERMEDIO, 'Intermedio'),
        (AVANZADO, 'Avanzado'),
        (OTRO, 'Otro'),
    ]

    diseno_id = models.AutoField(primary_key=True)
    profesor_id = models.IntegerField(Profesores, on_delete=models.CASCADE, related_name='experienciaDiseno', db_column='profesor_id')
    organizacion = models.TextField()
    periodo = models.TextField()
    nivel_experiencia = models.CharField(max_length=20, choices=NIVEL_EXPERIENCIA_CHOICES, default=BASICO)
    descripcion = models.TextField()
    created_at = models.DateField()
    updated_at = models.DateField()

    def __str__(self):
        return f"Profesor(x) {self.profesor_id} tiene experiencia de diseño de {self.diseno_id}"


class LogrosProfesionales():
    LOCAL = 1
    NACIONAL = 2
    INTERNACIONAL = 3
    OTRO = 4

    RELEVANCIA_CHOICES = [
        (LOCAL, 'Local'),
        (NACIONAL, 'Nacional'),
        (INTERNACIONAL, 'Internacional'),
        (OTRO, 'Otro'),
    ]

    logro_id = models.AutoField(primary_key=True)
    profesor_id = models.IntegerField(Profesores, on_delete=models.CASCADE, related_name='logrosProfesionales', db_column='profesor_id')
    descripcion = models.TextField()
    anno = models.IntegerField()
    relevancia = models.CharField(max_length=20, choices=RELEVANCIA_CHOICES, default=LOCAL)
    created_at = models.DateField()
    updated_at = models.DateField()

    def __str__(self):
        return f"Profesor(x) {self.profesor_id} tiene formacion academica de {self.nivel}"


class PremiosDistinciones():
    premio_id = models.AutoField(primary_key=True)
    profesor_id = models.IntegerField(Profesores, on_delete=models.CASCADE, related_name='premiosDistinciones', db_column='profesor_id')
    descripcion = models.TextField()
    anno = models.IntegerField()
    institucion_otorga = models.TextField()
    created_at = models.DateField()
    updated_at = models.DateField()

    def __str__(self):
        return f"Profesor(x) {self.profesor_id} tiene el premio de {self.premio_id}"

class ParticipacionOrganizaciones():
    MIEMBRO = 1
    COORDINADOR = 2
    PRESIDENTE = 3
    OTRO = 4

    NIVEL_PARTICIPACION_CHOICES = [
        (MIEMBRO, 'Miembro'),
        (COORDINADOR, 'Coordinador'),
        (PRESIDENTE, 'Presidente'),
        (OTRO, 'Otro'),
    ]

    participacion_id = models.AutoField(primary_key=True)
    profesor_id = models.IntegerField(Profesores, on_delete=models.CASCADE, related_name='participacionesOrganizaciones', db_column='profesor_id')
    organizacion = models.TextField()
    periodo = models.TextField()
    nivel_participacion = models.CharField(max_length=20, choices=NIVEL_PARTICIPACION_CHOICES, default=MIEMBRO)
    created_at = models.DateField()
    updated_at = models.DateField()

    def __str__(self):
        return f"Profesor(x) {self.profesor_id} participó en de {self.organizacion}"


class CapacitacionDocente():
    capacitacion_id = models.AutoField(primary_key=True)
    profesor_id = models.IntegerField(Profesores, on_delete=models.CASCADE, related_name='capacitacionDocente', db_column='profesor_id')
    nombre_curso = models.TextField()
    institucion = models.TextField()
    pais = models.TextField()
    anno_obtencion = models.IntegerField()
    horas = models.IntegerField()
    created_at = models.DateField()
    updated_at = models.DateField()

    def __str__(self):
        return f"Profesor(x) {self.profesor_id} recibió esta capacitación {self.capacitacion_id}"

class ActualizacionDisciplinar():
    actualizacion_id = models.AutoField(primary_key=True)
    profesor_id = models.IntegerField(Profesores, on_delete=models.CASCADE, related_name='actualizacionDisciplinar', db_column='profesor_id')
    nombre_curso = models.TextField()
    institucion = models.TextField()
    pais = models.TextField()
    anno_obtencion = models.IntegerField()
    horas = models.IntegerField()
    created_at = models.DateField()
    updated_at = models.DateField()

    def __str__(self):
        return f"Profesor(x) {self.profesor_id} recibió esta actualización disciplinar {self.actualizacion_id}"


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
    descripcion = models.TextField(blank=True, null=True)
    anno = models.PositiveSmallIntegerField()
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default=PUBLICACION)
    detalles = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Producto {self.producto_id} - {self.anno}"
