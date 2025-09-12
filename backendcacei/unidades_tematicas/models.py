from django.db import models

# Create your models here.
class UnidadTematica(models.Model):
    unidad_id = models.AutoField(primary_key=True)
    # Relación con curso_id
    numero = models.IntegerField(unique=True)
    descripcion = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.numero)
