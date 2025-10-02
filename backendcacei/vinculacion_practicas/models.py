from django.db import models

# Create your models here.
class Practica(models.Model):
    practica_id = models.AutoField(primary_key=True)
    curso_id = models.ForeignKey('core.Curso', on_delete=models.PROTECT, related_name='practicas', db_column='curso_id')
    numero = models.IntegerField()
    descripcion = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Práctica {self.numero}"
