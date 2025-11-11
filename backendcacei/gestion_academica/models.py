from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class UnidadTematica(models.Model):
    curso = models.ForeignKey('core.Curso', on_delete=models.PROTECT)
    
    numero = models.IntegerField(unique=True)
    descripcion = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.numero)

class ObjetivoEducacional(models.Model):
    programa = models.ForeignKey('core.ProgramaEducativo', on_delete=models.PROTECT)
    
    codigo = models.CharField(max_length=10, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.codigo

class AtributoPE(models.Model):
    programa = models.ForeignKey('core.ProgramaEducativo', on_delete=models.PROTECT)
    
    codigo = models.CharField(max_length=10, unique=True)
    nombre = models.CharField(max_length=100)
    nombre_abreviado = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.codigo

class CriterioDesempeno(models.Model):
    atributo_pe = models.ForeignKey(AtributoPE, on_delete=models.PROTECT)
    
    codigo = models.CharField(max_length=10, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.codigo

class EjeConocimiento(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.nombre

class EstrategiaEnsenanza(models.Model):
    curso = models.ForeignKey('core.Curso', on_delete=models.PROTECT)
    
    numero = models.IntegerField()
    descripcion = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.numero)

class EstrategiaEvaluacion(models.Model):
    curso = models.ForeignKey('core.Curso', on_delete=models.PROTECT)

    numero = models.IntegerField()
    descripcion = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.numero)

class Bibliografia(models.Model):
    curso = models.ForeignKey('core.Curso', on_delete=models.PROTECT)
    
    numero = models.IntegerField()
    autor = models.CharField(max_length=100)
    titulo = models.CharField(max_length=200)
    editorial = models.CharField(max_length=100)
    anio_publicacion = models.PositiveSmallIntegerField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.numero}. {self.autor} - {self.titulo} ({self.anio_publicacion})"

class HorasSemana(models.Model):
    curso = models.ForeignKey('core.Curso', on_delete=models.PROTECT)
    
    horas_totales = models.PositiveSmallIntegerField()
    horas_aula = models.PositiveSmallIntegerField()
    horas_laboratorio = models.PositiveSmallIntegerField()
    horas_practicas = models.PositiveSmallIntegerField()
    numero_grupos = models.PositiveSmallIntegerField()
    calificacion_promedio = models.DecimalField(max_digits=3, decimal_places=1)
    porcentaje_aprobacion = models.DecimalField(max_digits=5, decimal_places=2)
    porcentaje_reprobacion = models.DecimalField(max_digits=5, decimal_places=2)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Horas Totales: {self.horas_totales}"

class ObjetivoEspecifico(models.Model):
    curso = models.ForeignKey('core.Curso', on_delete=models.PROTECT)
    
    descripcion = models.TextField(blank=True, null=True)
    orden = models.IntegerField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.id)

class AtributoCACEI(models.Model):
    codigo = models.CharField(max_length=10, unique=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    wk_referencia = models.CharField(max_length=20, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.codigo

class CursoAtributoPE(models.Model):
    curso = models.ForeignKey('core.Curso', on_delete=models.PROTECT)
    atributo_pe = models.ForeignKey(AtributoPE, on_delete=models.PROTECT)
    
    nivel_aporte = models.CharField(max_length=1, choices=[('I', 'Introductorio'), ('M', 'Medio'), ('A', 'Avanzado')], default='I')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CursoEje(models.Model):
    curso = models.ForeignKey('core.Curso', on_delete=models.PROTECT)
    eje = models.ForeignKey(EjeConocimiento, on_delete=models.PROTECT)

    horas = models.PositiveSmallIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class AtributoPEObjetivo(models.Model):
    atributo_pe = models.ForeignKey(AtributoPE, on_delete=models.PROTECT)
    objetivo = models.ForeignKey(ObjetivoEducacional, on_delete=models.PROTECT)
    
    justificacion = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class AtributoPECACEI(models.Model):
    atributo_pe = models.ForeignKey(AtributoPE, on_delete=models.PROTECT)
    atributo_cacei = models.ForeignKey(AtributoCACEI, on_delete=models.PROTECT)

    justificacion = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Practica(models.Model):
    curso = models.ForeignKey('core.Curso', on_delete=models.PROTECT)

    numero = models.IntegerField()
    descripcion = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Práctica {self.numero}"

class Alumno(models.Model):
    matricula = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=50)
    apellido1 = models.CharField(max_length=50)
    apellido2 = models.CharField(max_length=50, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.matricula} - {self.nombre} {self.apellido1} {self.apellido2 or ''}"

class Calificacion(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.PROTECT)
    profesor_curso = models.ForeignKey('gestion_de_profesores.ProfesorCurso', on_delete=models.PROTECT)

    valor = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Calificación del alumno entre 0 y 100"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.alumno.matricula} - {self.valor}"
