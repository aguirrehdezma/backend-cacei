from django.db import models

# Create your models here.
class Hallazgo(models.Model):
    hallazgo_id = models.AutoField(primary_key=True)
    programa_id = models.ForeignKey('core.ProgramaEducativo', on_delete=models.PROTECT, related_name='hallazgos', db_column='programa_id')
    numero_hallazgo = models.IntegerField()
    descripcion = models.TextField()
    objetivo_id = models.ForeignKey('gestion_academica.ObjetivoEducacional', on_delete=models.PROTECT, related_name='hallazgos', db_column='objetivo_id', null=True, blank=True)
    atributo_pe_id = models.ForeignKey('gestion_academica.AtributoPE', on_delete=models.PROTECT, related_name='hallazgos', db_column='atributo_pe_id', null=True, blank=True)
    es_indice_rendimiento = models.BooleanField(default=False)
    indicador_mr2025 = models.CharField(max_length=50, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Hallazgo {self.numero_hallazgo}"

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
    hallazgo_id = models.ForeignKey(Hallazgo, on_delete=models.PROTECT, related_name='acciones_mejora', db_column='hallazgo_id')
    descripcion = models.TextField()
    resultado_esperado = models.TextField()
    meta = models.TextField()
    fecha_meta = models.DateField()
    responsable = models.CharField(max_length=100)
    estatus = models.CharField(max_length=20, choices=ESTATUS_CHOICES, default=PENDIENTE)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Acción de Mejora {self.accion_id} - {self.estatus}"

class Indicador(models.Model):
    indicador_id = models.AutoField(primary_key=True)
    criterio_id = models.ForeignKey('gestion_academica.CriterioDesempeno', on_delete=models.PROTECT, related_name='indicadores', db_column='criterio_id')
    codigo  = models.CharField(max_length=10)
    descripcion = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Indicador {self.codigo}"

class EvaluacionIndicador(models.Model):
    SI = 'si'
    NO = 'no'
    
    ESTADO_CHOICES = [
        (SI, 'Sí'),
        (NO, 'No'),
    ]
    
    evaluacion_id = models.AutoField(primary_key=True)
    indicador_id = models.ForeignKey(Indicador, on_delete=models.PROTECT, related_name='evaluaciones', db_column='indicador_id')
    curso_id = models.ForeignKey('core.Curso', on_delete=models.PROTECT, related_name='evaluaciones', db_column='curso_id')
    grupo_seccion = models.CharField(max_length=50)
    instrumento_evaluacion = models.CharField(max_length=100)
    descripcion_instrumento = models.TextField(null=True, blank=True)
    periodo_evaluacion = models.CharField(max_length=50)
    valoracion = models.CharField(max_length=2, choices=ESTADO_CHOICES)
    analisis_resultados = models.TextField(null=True, blank=True)
    meta = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class AportacionPE(models.Model):
    aportacion_id = models.AutoField(primary_key=True)
    profesor_id = models.ForeignKey('core.Profesor', on_delete=models.PROTECT, related_name='aportaciones_pe', db_column='profesor_id')
    descripcion = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Aportación PE {self.aportacion_id}"

class GestionAcademica(models.Model):
    gestion_id = models.AutoField(primary_key=True)
    profesor_id = models.ForeignKey('core.Profesor', on_delete=models.PROTECT, related_name='gestion_academica', db_column='profesor_id')
    institucion_id = models.ForeignKey('core.Institucion', on_delete=models.PROTECT, related_name='gestion_academica', db_column='institucion_id')
    actividad = models.CharField(max_length=100)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Gestión Académica {self.gestion_id} - {self.actividad}"

class Auditoria(models.Model):
    auditoria_id = models.AutoField(primary_key=True)
    # usuario_id
    accion = models.CharField(max_length=50)
    tabla_afectada = models.CharField(max_length=50)
    registro_id = models.IntegerField(null=True, blank=True)
    datos_anteriores = models.JSONField(null=True, blank=True)
    datos_nuevos = models.JSONField(null=True, blank=True)
    ip_address = models.CharField(max_length=45, null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Auditoría {self.auditoria_id} - {self.accion}"
