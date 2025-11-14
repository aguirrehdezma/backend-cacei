from django.db import models

from core.models import Curso, Periodo, ProgramaEducativo, Profesor

# Create your models here.
class Cedula(models.Model):
    ORGANIZACION_CURRICULAR = 'organizacion_curricular'
    CV_SINTETICO = 'cv_sintetico'

    TIPO_CHOICES = [
        (ORGANIZACION_CURRICULAR, 'Organización Curricular'),
        (CV_SINTETICO, 'CV Sintético'),
    ]
    
    programa = models.ForeignKey(ProgramaEducativo, on_delete=models.PROTECT, null=True, blank=True)
    periodo = models.ForeignKey(Periodo, on_delete=models.PROTECT, null=True, blank=True)
    profesor = models.ForeignKey(Profesor, on_delete=models.PROTECT, null=True, blank=True)
    
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES, default=ORGANIZACION_CURRICULAR)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        # Guardar la cédula primero
        super().save(*args, **kwargs)
        
        if self.tipo == Cedula.ORGANIZACION_CURRICULAR and self.programa:
            cursos = self.programa.curso_set.all()
            
            obligatorios = cursos.filter(tipo='obligatorio')
            optativos = cursos.filter(tipo='optativo')
            
            # Eliminar relaciones previas si estás actualizando
            CursoObligatorio.objects.filter(cedula=self).delete()
            CursoOptativo.objects.filter(cedula=self).delete()
            
            # Crear nuevas relaciones
            CursoObligatorio.objects.bulk_create([
                CursoObligatorio(cedula=self, curso=curso) for curso in obligatorios
            ])
            CursoOptativo.objects.bulk_create([
                CursoOptativo(cedula=self, curso=curso) for curso in optativos
            ])
    
    def __str__(self):
        return f"Cédula {self.tipo} - {self.programa.nombre} ({self.periodo.nombre})"

class CursoObligatorio(models.Model):
    cedula = models.ForeignKey(Cedula, on_delete=models.PROTECT)
    curso = models.ForeignKey(Curso, on_delete=models.PROTECT)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.curso.nombre} (Obligatorio)"

class CursoOptativo(models.Model):
    cedula = models.ForeignKey(Cedula, on_delete=models.PROTECT)
    curso = models.ForeignKey(Curso, on_delete=models.PROTECT)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.curso.nombre} (Optativo)"
