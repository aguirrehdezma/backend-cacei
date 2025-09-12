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
