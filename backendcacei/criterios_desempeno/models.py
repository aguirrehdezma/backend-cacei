from django.db import models

# Create your models here.
class CriterioDesempeno(models.Model):
    criterio_id = models.AutoField(primary_key=True)
    # Relación con atributo_pe_id
    codigo = models.CharField(max_length=10, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.codigo