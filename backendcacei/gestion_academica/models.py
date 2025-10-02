from django.db import models

# Create your models here.
class UnidadTematica(models.Model):
    unidad_id = models.AutoField(primary_key=True)
    curso_id = models.ForeignKey('core.Curso', on_delete=models.PROTECT, related_name='unidades_tematicas', db_column='curso_id')
    numero = models.IntegerField(unique=True)
    descripcion = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.numero)

class ObjetivoEducacional(models.Model):
    objetivo_id = models.AutoField(primary_key=True)
    programa_id = models.ForeignKey('core.ProgramaEducativo', on_delete=models.PROTECT, related_name='objetivos_educacionales', db_column='programa_id')
    codigo = models.CharField(max_length=10, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.codigo

class AtributoPE(models.Model):
    atributo_pe_id = models.AutoField(primary_key=True)
    programa_id = models.ForeignKey('core.ProgramaEducativo', on_delete=models.PROTECT, related_name='atributos_pe', db_column='programa_id')
    codigo = models.CharField(max_length=10, unique=True)
    nombre = models.CharField(max_length=100)
    nombre_abreviado = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.codigo

class CriterioDesempeno(models.Model):
    criterio_id = models.AutoField(primary_key=True)
    atributo_pe_id = models.ForeignKey(AtributoPE, on_delete=models.PROTECT, related_name='criterios_desempeno', db_column='atributo_pe_id')
    codigo = models.CharField(max_length=10, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.codigo

class EjeConocimiento(models.Model):
    eje_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.nombre

class EstrategiaEnsenanza(models.Model):
    estrategia_id = models.AutoField(primary_key=True)
    curso_id = models.ForeignKey('core.Curso', on_delete=models.PROTECT, related_name='estrategias_ensenanza', db_column='curso_id')
    numero = models.IntegerField()
    descripcion = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.numero)

class EstrategiaEvaluacion(models.Model):
    estrategia_id = models.AutoField(primary_key=True)
    curso_id = models.ForeignKey('core.Curso', on_delete=models.PROTECT, related_name='estrategias_evaluacion', db_column='curso_id')
    numero = models.IntegerField()
    descripcion = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.numero)

class Bibliografia(models.Model):
    bibliografia_id = models.AutoField(primary_key=True)
    curso_id = models.ForeignKey('core.Curso', on_delete=models.PROTECT, related_name='bibliografias', db_column='curso_id')
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
    horas_id = models.AutoField(primary_key=True)
    curso_id = models.ForeignKey('core.Curso', on_delete=models.PROTECT, related_name='horas_semana', db_column='curso_id')
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
    objetivo_id = models.AutoField(primary_key=True)
    curso_id = models.ForeignKey('core.Curso', on_delete=models.PROTECT, related_name='objetivos_especificos', db_column='curso_id')
    descripcion = models.TextField(blank=True, null=True)
    orden = models.IntegerField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.objetivo_id)

class AtributoCACEI(models.Model):
    atributo_cacei_id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=10, unique=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    wk_referencia = models.CharField(max_length=20, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.codigo

class CursoAtributoPE(models.Model):
    curso_atributo_pe_id = models.AutoField(primary_key=True)
    curso_id = models.ForeignKey('core.Curso', on_delete=models.PROTECT, related_name='curso_atributo_pe', db_column='curso_id')
    atributo_pe_id = models.ForeignKey(AtributoPE, on_delete=models.PROTECT, related_name='curso_atributo_pe', db_column='atributo_pe_id')
    nivel_aporte = models.CharField(max_length=1, choices=[('I', 'Introductorio'), ('M', 'Medio'), ('A', 'Avanzado')], default='I')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CursoEje(models.Model):
    curso_eje_id = models.AutoField(primary_key=True)
    curso_id = models.ForeignKey('core.Curso', on_delete=models.PROTECT, related_name='curso_eje', db_column='curso_id')
    eje_id = models.ForeignKey(EjeConocimiento, on_delete=models.PROTECT, related_name='curso_eje', db_column='eje_id')
    horas = models.PositiveSmallIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class AtributoPEObjetivo(models.Model):
    atributo_pe_objetivo_id = models.AutoField(primary_key=True)
    atributo_pe_id = models.ForeignKey(AtributoPE, on_delete=models.PROTECT, related_name='atributo_pe_objetivo', db_column='atributo_pe_id')
    objetivo_id = models.ForeignKey(ObjetivoEducacional, on_delete=models.PROTECT, related_name='atributo_pe_objetivo', db_column='objetivo_id')
    justificacion = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class AtributoPECACEI(models.Model):
    atributo_pe_cacei_id = models.AutoField(primary_key=True)
    atributo_pe_id = models.ForeignKey(AtributoPE, on_delete=models.PROTECT, related_name='atributo_pe_cacei', db_column='atributo_pe_id')
    atributo_cacei_id = models.ForeignKey(AtributoCACEI, on_delete=models.PROTECT, related_name='atributo_pe_cacei', db_column='atributo_cacei_id')
    justificacion = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Practica(models.Model):
    practica_id = models.AutoField(primary_key=True)
    curso_id = models.ForeignKey('core.Curso', on_delete=models.PROTECT, related_name='practicas', db_column='curso_id')
    numero = models.IntegerField()
    descripcion = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Práctica {self.numero}"
