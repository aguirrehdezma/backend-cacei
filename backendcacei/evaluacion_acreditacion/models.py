from django.db import models

# Create your models here.
class Hallazgo(models.Model):
    programa = models.ForeignKey('core.ProgramaEducativo', on_delete=models.PROTECT)
    objetivo = models.ForeignKey('gestion_academica.ObjetivoEducacional', on_delete=models.PROTECT, null=True, blank=True)
    atributo_pe = models.ForeignKey('gestion_academica.AtributoPE', on_delete=models.PROTECT, null=True, blank=True)
    
    numero_hallazgo = models.IntegerField()
    descripcion = models.TextField()
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

    hallazgo = models.ForeignKey(Hallazgo, on_delete=models.PROTECT)
    
    descripcion = models.TextField()
    resultado_esperado = models.TextField()
    meta = models.TextField()
    fecha_meta = models.DateField()
    responsable = models.CharField(max_length=100)
    estatus = models.CharField(max_length=20, choices=ESTATUS_CHOICES, default=PENDIENTE)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Acción de Mejora {self.id} - {self.estatus}"

class Indicador(models.Model):
    criterio = models.ForeignKey('gestion_academica.CriterioDesempeno', on_delete=models.PROTECT)
    
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
    
    indicador = models.ForeignKey(Indicador, on_delete=models.PROTECT)
    curso = models.ForeignKey('core.Curso', on_delete=models.PROTECT)
    
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
    profesor = models.ForeignKey('core.Profesor', on_delete=models.PROTECT)

    descripcion = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Aportación PE {self.id}"

class GestionAcademica(models.Model):
    profesor = models.ForeignKey('core.Profesor', on_delete=models.PROTECT)
    institucion = models.ForeignKey('core.Institucion', on_delete=models.PROTECT)
    
    actividad = models.CharField(max_length=100)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Gestión Académica {self.id} - {self.actividad}"

class Auditoria(models.Model):
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
        return f"Auditoría {self.id} - {self.accion}"
