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
    