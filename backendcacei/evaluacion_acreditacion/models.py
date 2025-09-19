from django.db import models

class AccionMejora(models.Model): 
    PENDIENTE = 'pendiente'
    EN_PROGRESO = 'en_progreso'
    COMPLETADA = 'completada'
    CANCELADA = 'cancelada'

    ESTATUS_CHOICES = [
        (PENDIENTE, 'Pendiente'),
        (EN_PROGRESO, 'En Progreso'),
        (COMPLETADA, 'Completada'),
        (CANCELADA, 'Cancelada'),
    ]
    accion_id = models.AutoField(primary_key=True)
    #hallazgo_id
    descripcion = models.TextField()
    resultado_esperado = models.TextField()
    meta = models.TextField()
    fecha_meta = models.DateField()
    responsable = models.CharField(max_length=100)
    estatus = models.CharField(max_length=20, choices=ESTATUS_CHOICES, default=PENDIENTE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
# Create your models here.

class Indicador(models.Model):
    indicador_id = models.AutoField(primary_key=True)
    #criterio_id = models.ForeignKey('gestion_academica.CriterioDesempeno', on_delete=models.CASCADE)
    codigo  = models.CharField(max_length=10)
    descripcion = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Evaluacion_Indicador (models.Model):
    SI = 'si'
    NO = 'no'
    ESTADO_CHOICES = [
        (SI, 'Sí'),
        (NO, 'No'),
    ]
    evaluacion_id = models.AutoField(primary_key=True)
    #indicador_id = models.ForeignKey(Indicador, on_delete=models.CASCADE)
    #curso_id = models.ForeignKey('gestion_academica.Curso', on_delete=models.CASCADE)
    grupo_seccion = models.CharField(max_length=50)
    instrumento_evaluacion = models.CharField(max_length=100)
    descripcion_instrumento = models.TextField()
    periodo_evaluacion = models.CharField(max_length=50)
    valoracion = models.CharField(max_length=2, choices=ESTADO_CHOICES)
    analisis_resultados = models.TextField()
    meta = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class aportacion_pe(models.Model):
    aportacion_id = models.AutoField(primary_key=True)
    #profesor_id = models.ForeignKey('gestion_academica.Profesor', on_delete=models.CASCADE)
    descripcion = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Gestion_Academica(models.Model):
    gestion_id = models.AutoField(primary_key=True)
    #profesor_id = models.ForeignKey('gestion_academica.Profesor', on_delete=models.CASCADE)
    actividad = models.CharField(max_length=100)
    institucion = models.CharField(max_length=100)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Hallazgo(models.Model):
    hallazgo_id = models.AutoField(primary_key=True)
    #programa_id = models.ForeignKey('gestion_academica.ProgramaEducativo', on_delete=models.CASCADE)
    numero_hallazgo = models.IntegerField()
    descripcion = models.TextField()
    objetivo_id = models.IntegerField()
    atributo_pe_id = models.IntegerField()
    es_indice_rendimiento = models.BooleanField()
    indicador_mr2025 = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Auditoria(models.Model):
    auditoria_id = models.AutoField(primary_key=True)
    usuario_id = models.IntegerField()
    accion = models.CharField(max_length=50)
    tabla_afectada = models.CharField(max_length=50)
    registro_id = models.IntegerField()
    datos_anteriores = models.JSONField(null=True, blank=True)
    datos_nuevos = models.JSONField(null=True, blank=True)
    ip_address = models.CharField(max_length=45)
    user_agent = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



