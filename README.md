# BackendCacei
## Carpeta Cedulas
###init.py
<p>
Esta clase sirve como un iniciador del la carpeta.
</p>

```python

```
###admin.py
<p>
Esta clase sirve para registrar las páginas de la carpeta.
</p>

```python
from django.contrib import admin

from cedulas.models import Cedula

# Register your models here.
admin.site.register(Cedula)
```
###apps.py
<p>
Esta clase sirve para importar el django para las páginas.
</p>

```python
from django.apps import AppConfig


class CedulasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cedulas'
```
###models.py
<p>
Esta clase sirve para importar los datos de la base de datos a las páginas.
</p>

```python
from django.db import models
from django.db.models import Avg

from gestion_academica.models import Calificacion
from gestion_de_profesores.models import ProfesorCurso
from core.models import Curso

# Create your models here.
class Cedula(models.Model):
    ORGANIZACION_CURRICULAR = 'organizacion_curricular'
    CV_SINTETICO = 'cv_sintetico'
    PLAN_MEJORA = 'plan_mejora'
    VALORACION_OBJETIVOS = 'valoracion_objetivos'
    AEP_VS_AECACEI = 'aep_vs_aecacei'
    AEP_VS_OE = 'aep_vs_oe'
    CURSOS_VS_AEP = 'cursos_vs_aep'
    HERRAMIENTAS_VALORACION_AEP = 'herramientas_valoracion_aep'
    PROGRAMA_ASIGNATURA = 'programa_asignatura'
    
    TIPO_CHOICES = [
        (ORGANIZACION_CURRICULAR, 'Organización Curricular'),
        (CV_SINTETICO, 'CV Sintético'),
        (PLAN_MEJORA, 'Plan de Mejora'),
        (VALORACION_OBJETIVOS, 'Valoración de Objetivos'),
        (AEP_VS_AECACEI, 'AEP vs AE-CACEI'),
        (AEP_VS_OE, 'AEP vs OE'),
        (CURSOS_VS_AEP, 'Cursos vs AEP'),
        (HERRAMIENTAS_VALORACION_AEP, 'Herramientas de Valoración de AEP'),
        (PROGRAMA_ASIGNATURA, 'Programa de Asignatura'),
    ]
    
    programa = models.ForeignKey('core.ProgramaEducativo', on_delete=models.PROTECT, null=True, blank=True)
    periodo = models.ForeignKey('core.Periodo', on_delete=models.PROTECT)
    profesor = models.ForeignKey('core.Profesor', on_delete=models.PROTECT, null=True, blank=True)
    
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES, default=ORGANIZACION_CURRICULAR)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        # Guardar la cédula primero
        super().save(*args, **kwargs)
        
        if self.tipo == Cedula.ORGANIZACION_CURRICULAR and self.programa:
            cursos = Curso.objects.filter(
                programa=self.programa,
                profesorcurso__periodo=self.periodo
            ).distinct()
            
            obligatorios = cursos.filter(tipo='obligatorio')
            optativos = cursos.filter(tipo='optativo')
            curriculares = cursos.filter(tipo="curricular")
            
            # Eliminar relaciones previas si estás actualizando
            CursoObligatorioEje.objects.filter(curso_obligatorio__cedula=self).delete()
            CursoOptativoEje.objects.filter(curso_optativo__cedula=self).delete()
            CursoCurricularEje.objects.filter(curso_curricular__cedula=self).delete()
            
            CursoObligatorio.objects.filter(cedula=self).delete()
            CursoOptativo.objects.filter(cedula=self).delete()
            CursoCurricular.objects.filter(cedula=self).delete()
            
            # Crear nuevas relaciones 
            for curso in obligatorios:
                co = CursoObligatorio.objects.create(
                    cedula=self,
                    curso=curso,
                )
                for relacion in curso.cursoeje_set.all():
                    CursoObligatorioEje.objects.create(
                        curso_obligatorio=co,
                        eje=relacion.eje,
                        nombre_eje=relacion.eje.nombre,
                        horas=relacion.horas,
                    )
            
            for curso in optativos:
                co = CursoOptativo.objects.create(
                    cedula=self,
                    curso=curso,
                )
                for relacion in curso.cursoeje_set.all():
                    CursoOptativoEje.objects.create(
                        curso_optativo=co,
                        eje=relacion.eje,
                        nombre_eje=relacion.eje.nombre,
                        horas=relacion.horas,
                    )
            
            for curso in curriculares:
                cc = CursoCurricular.objects.create(
                    cedula=self,
                    curso=curso,
                )
                for relacion in curso.cursoeje.all():
                    CursoCurricularEje.objects.create(
                        curso_curricular=cc,
                        eje=relacion.eje,
                        nombre_eje=relacion.eje.nombre,
                        horas=relacion.horas
                    )
        
        if self.tipo == Cedula.CV_SINTETICO and self.profesor:
            ActualizacionDisciplinarCedula.objects.filter(cedula=self).delete()
            FormacionAcademicaCedula.objects.filter(cedula=self).delete()
            CapacitacionDocenteCedula.objects.filter(cedula=self).delete()
            ExperienciaProfesionalCedula.objects.filter(cedula=self).delete()
            ExperienciaDisenoCedula.objects.filter(cedula=self).delete()
            LogroProfesionalCedula.objects.filter(cedula=self).delete()
            ParticipacionOrganizacionesCedula.objects.filter(cedula=self).delete()
            PremioDistincionCedula.objects.filter(cedula=self).delete()
            ProductoAcademicoCedula.objects.filter(cedula=self).delete()
            AportacionPECedula.objects.filter(cedula=self).delete()
            GestionAcademicaCedula.objects.filter(cedula=self).delete()
            
            # Crear snapshots de las relaciones actuales del profesor
            ActualizacionDisciplinarCedula.objects.bulk_create([
                ActualizacionDisciplinarCedula(cedula=self, actualizacion=a)
                for a in self.profesor.actualizaciondisciplinar_set.all()
            ])
            FormacionAcademicaCedula.objects.bulk_create([
                FormacionAcademicaCedula(cedula=self, formacion=f)
                for f in self.profesor.formacionacademica_set.all()
            ])
            CapacitacionDocenteCedula.objects.bulk_create([
                CapacitacionDocenteCedula(cedula=self, capacitacion=c)
                for c in self.profesor.capacitaciondocente_set.all()
            ])
            ExperienciaProfesionalCedula.objects.bulk_create([
                ExperienciaProfesionalCedula(cedula=self, experiencia=e)
                for e in self.profesor.experienciaprofesional_set.all()
            ])
            ExperienciaDisenoCedula.objects.bulk_create([
                ExperienciaDisenoCedula(cedula=self, experiencia=e)
                for e in self.profesor.experienciadiseno_set.all()
            ])
            LogroProfesionalCedula.objects.bulk_create([
                LogroProfesionalCedula(cedula=self, logro=l)
                for l in self.profesor.logroprofesional_set.all()
            ])
            ParticipacionOrganizacionesCedula.objects.bulk_create([
                ParticipacionOrganizacionesCedula(cedula=self, participacion=p)
                for p in self.profesor.participacionorganizaciones_set.all()
            ])
            PremioDistincionCedula.objects.bulk_create([
                PremioDistincionCedula(cedula=self, premio=pr)
                for pr in self.profesor.premiodistincion_set.all()
            ])
            ProductoAcademicoCedula.objects.bulk_create([
                ProductoAcademicoCedula(cedula=self, producto=pa)
                for pa in self.profesor.productoacademico_set.all()
            ])
            AportacionPECedula.objects.bulk_create([
                AportacionPECedula(cedula=self, aportacion=ap)
                for ap in self.profesor.aportacionpe_set.all()
            ])
            GestionAcademicaCedula.objects.bulk_create([
                GestionAcademicaCedula(cedula=self, gestion=g)
                for g in self.profesor.gestionacademica_set.all()
            ])
        
        if self.tipo == Cedula.PLAN_MEJORA and self.programa:
            # Limpiar snapshots previos
            HallazgoCedula.objects.filter(cedula=self).delete()
            AccionMejoraCedula.objects.filter(cedula=self).delete()
            
            # Congelar hallazgos
            hallazgos = self.programa.hallazgo_set.all()
            HallazgoCedula.objects.bulk_create([
                HallazgoCedula(cedula=self, hallazgo=h) for h in hallazgos
            ])
            
            # Congelar acciones de mejora ligadas a cada hallazgo
            acciones = []
            for h in hallazgos:
                for a in h.accionmejora_set.all():
                    acciones.append(AccionMejoraCedula(cedula=self, hallazgo=h, accion=a))
            AccionMejoraCedula.objects.bulk_create(acciones)
        
        if self.tipo == Cedula.VALORACION_OBJETIVOS and self.programa:
            # Limpiar snapshots previos
            ObjetivoEducacionalCedula.objects.filter(cedula=self).delete()
            AtributoObjetivoCedula.objects.filter(cedula=self).delete()
            CriterioDesempenoCedula.objects.filter(cedula=self).delete()
            IndicadorCedula.objects.filter(cedula=self).delete()
            EvaluacionIndicadorCedula.objects.filter(cedula=self).delete()
            
            # Congelar objetivos
            objetivos = self.programa.objetivoeducacional_set.all()
            ObjetivoEducacionalCedula.objects.bulk_create([
                ObjetivoEducacionalCedula(cedula=self, objetivo=o) for o in objetivos
            ])
            
            atributos, criterios, indicadores, evaluaciones = [], [], [], []
            
            for o in objetivos:
                # Paso por atributos_pe_objetivos
                for rel in o.atributopeobjetivo_set.all():
                    atributos.append(AtributoObjetivoCedula(cedula=self, objetivo=o, atributo=rel.atributo_pe))
                    # Desde atributo_pe llego a criterios
                    for c in rel.atributo_pe.criteriodesempeno_set.all():
                        criterios.append(CriterioDesempenoCedula(cedula=self, atributo=rel.atributo_pe, criterio=c))
                        # Desde criterio llego a indicadores
                        for i in c.indicador_set.all():
                            indicadores.append(IndicadorCedula(cedula=self, criterio=c, indicador=i))
                            # Desde indicador llego a evaluaciones
                            for e in i.evaluacionindicador_set.all():
                                evaluaciones.append(EvaluacionIndicadorCedula(cedula=self, indicador=i, evaluacion=e))
            
            AtributoObjetivoCedula.objects.bulk_create(atributos)
            CriterioDesempenoCedula.objects.bulk_create(criterios)
            IndicadorCedula.objects.bulk_create(indicadores)
            EvaluacionIndicadorCedula.objects.bulk_create(evaluaciones)
        
        if self.tipo == Cedula.AEP_VS_AECACEI and self.programa:
            # Limpiar snapshots previos
            AtributoPECedula.objects.filter(cedula=self).delete()
            AtributoPECACEICedula.objects.filter(cedula=self).delete()
            
            # Congelar atributos PE del programa
            atributos_pe = self.programa.atributope_set.all()
            AtributoPECedula.objects.bulk_create([
                AtributoPECedula(cedula=self, atributo_pe=a) for a in atributos_pe
            ])
            
            # Congelar relaciones con atributos CACEI
            relaciones = []
            for a in atributos_pe:
                for rel in a.atributopecacei_set.all():
                    relaciones.append(
                        AtributoPECACEICedula(
                            cedula=self,
                            atributo_pe=a,
                            atributo_cacei=rel.atributo_cacei,
                            relacion=rel
                        )
                    )
            AtributoPECACEICedula.objects.bulk_create(relaciones)
        
        if self.tipo == Cedula.AEP_VS_OE and self.programa:
            # Limpiar snapshots previos
            AtributoPECedula.objects.filter(cedula=self).delete()
            AtributoObjetivoCedulaAEPVsOE.objects.filter(cedula=self).delete()
            
            # Congelar atributos PE del programa
            atributos_pe = self.programa.atributope_set.all()
            AtributoPECedula.objects.bulk_create([
                AtributoPECedula(cedula=self, atributo_pe=a) for a in atributos_pe
            ])
            
            # Congelar relaciones con objetivos educacionales
            relaciones = []
            for a in atributos_pe:
                for rel in a.atributopeobjetivo_set.all():
                    relaciones.append(
                        AtributoObjetivoCedulaAEPVsOE(
                            cedula=self,
                            atributo_pe=a,
                            objetivo=rel.objetivo,
                            relacion=rel
                        )
                    )
            AtributoObjetivoCedulaAEPVsOE.objects.bulk_create(relaciones)
        
        if self.tipo == Cedula.CURSOS_VS_AEP and self.programa:
            # Limpiar snapshots previos
            CursoCedula.objects.filter(cedula=self).delete()
            CursoAtributoPECedula.objects.filter(cedula=self).delete()
            
            # Congelar cursos del programa
            cursos = self.programa.curso_set.all()
            CursoCedula.objects.bulk_create([
                CursoCedula(cedula=self, curso=c) for c in cursos
            ])
            
            # Congelar relaciones curso - atributos PE
            relaciones = []
            for c in cursos:
                for rel in c.cursoatributope_set.all():
                    relaciones.append(
                        CursoAtributoPECedula(
                            cedula=self,
                            curso=c,
                            atributo_pe=rel.atributo_pe,
                            relacion=rel,
                            nombre_abreviado=rel.atributo_pe.nombre_abreviado,
                            nivel_aporte=rel.nivel_aporte
                        )
                    )
            CursoAtributoPECedula.objects.bulk_create(relaciones)
        
        if self.tipo == Cedula.HERRAMIENTAS_VALORACION_AEP and self.programa:
            # Limpiar snapshots previos
            AtributoPECedula.objects.filter(cedula=self).delete()
            CriterioDesempenoCedula.objects.filter(cedula=self).delete()
            IndicadorCedula.objects.filter(cedula=self).delete()
            EvaluacionIndicadorCedula.objects.filter(cedula=self).delete()
            
            # Congelar atributos PE del programa
            atributos_pe = self.programa.atributope_set.all()
            AtributoPECedula.objects.bulk_create([
                AtributoPECedula(cedula=self, atributo_pe=a) for a in atributos_pe
            ])
            
            criterios, indicadores, evaluaciones = [], [], []
            
            for a in atributos_pe:
                # Desde atributo llego a criterios
                for c in a.criteriodesempeno_set.all():
                    criterios.append(
                        CriterioDesempenoCedula(
                            cedula=self,
                            atributo_pe=a,
                            criterio=c
                        )
                    )
                    # Desde criterio llego a indicadores
                    for i in c.indicador_set.all():
                        indicadores.append(
                            IndicadorCedula(
                                cedula=self,
                                criterio=c,
                                indicador=i
                            )
                        )
                        # Desde indicador llego a evaluaciones
                        for e in i.evaluacionindicador_set.all():
                            evaluaciones.append(
                                EvaluacionIndicadorCedula(
                                    cedula=self,
                                    indicador=i,
                                    evaluacion=e
                                )
                            )
            
            # Guardar snapshots en bloque
            CriterioDesempenoCedula.objects.bulk_create(criterios)
            IndicadorCedula.objects.bulk_create(indicadores)
            EvaluacionIndicadorCedula.objects.bulk_create(evaluaciones)
        
        if self.tipo == Cedula.PROGRAMA_ASIGNATURA and self.programa and self.curso:            
            # Limpiar snapshots previos
            CursoInfoCedula.objects.filter(cedula=self).delete()
            CursoEjeCedula.objects.filter(cedula=self).delete()
            CursoObjetivoEspecificoCedula.objects.filter(cedula=self).delete()
            CursoAtributoPECedula.objects.filter(cedula=self).delete()
            HorasSemanaCedula.objects.filter(cedula=self).delete()
            CursoEstadisticasCedula.objects.filter(cedula=self).delete()
            UnidadTematicaCedula.objects.filter(cedula=self).delete()
            EstrategiaEnsenanzaCedula.objects.filter(cedula=self).delete()
            EstrategiaEvaluacionCedula.objects.filter(cedula=self).delete()
            PracticaCedula.objects.filter(cedula=self).delete()
            BibliografiaCedula.objects.filter(cedula=self).delete()
            ProfesorActualCedula.objects.filter(cedula=self).delete()
            ProfesorAnteriorCedula.objects.filter(cedula=self).delete()
            
            # Contar grupos (ProfesorCurso = cada grupo impartido en ese periodo)
            numero_grupos = ProfesorCurso.objects.filter(
                curso=self.curso,
                periodo=self.periodo
            ).count()
            
            # Congelar info básica del curso
            CursoInfoCedula.objects.create(
                cedula=self,
                clave=self.curso.clave,
                nombre=self.curso.nombre,
                seriacion=self.curso.seriacion,
                ubicacion=self.curso.ubicacion,
                tipo=self.curso.tipo,
                objetivo_general=self.curso.objetivo_general,
                numero_grupos=numero_grupos
            )
            
            # Congelar ejes del curso
            for relacion in self.curso.cursoeje_set.all():
                CursoEjeCedula.objects.create(
                    cedula=self,
                    eje=relacion.eje,
                    nombre_eje=relacion.eje.nombre,
                    horas=relacion.horas
                )
            
            # Congelar objetivos específicos
            for relacion in self.curso.objetivoespecifico_set.all():
                CursoObjetivoEspecificoCedula.objects.create(
                    cedula=self,
                    objetivo=relacion.objetivo,
                    descripcion=relacion.objetivo.descripcion
                )
            
            # Congelar relaciones atributos PE del curso
            for relacion in self.curso.cursoatributope_set.all():
                CursoAtributoPECedula.objects.create(
                    cedula=self,
                    curso=self.curso,
                    atributo_pe=relacion.atributo_pe,
                    relacion=relacion,
                    nombre_abreviado=relacion.atributo_pe.nombre_abreviado,
                    nivel_aporte=relacion.nivel_aporte
                )
            
            # Congelar horas por semana del curso
            for hs in self.curso.horasemana_set.all():
                HorasSemanaCedula.objects.create(
                    cedula=self,
                    horas_totales=hs.horas_totales,
                    horas_aula=hs.horas_aula,
                    horas_laboratorio=hs.horas_laboratorio,
                    horas_practicas=hs.horas_practicas
                )
            
            # Obtener todas las calificaciones de este curso en el periodo
            calificaciones = Calificacion.objects.filter(
                profesor_curso__curso=self.curso,
                profesor_curso__periodo=self.periodo
            )
            
            total = calificaciones.count()
            promedio = calificaciones.aggregate(prom=Avg('valor'))['prom'] or 0
            
            # % de calificaciones >= promedio
            mayores_iguales = calificaciones.filter(valor__gte=promedio).count()
            porcentaje_mayores_iguales = (mayores_iguales / total * 100) if total > 0 else 0
            
            # % de reprobados (< 70)
            reprobados = calificaciones.filter(valor__lt=70).count()
            porcentaje_reprobados = (reprobados / total * 100) if total > 0 else 0
            
            # Guardar snapshot de estadísticas
            CursoEstadisticasCedula.objects.create(
                cedula=self,
                promedio=round(promedio, 2),
                porcentaje_mayores_iguales=round(porcentaje_mayores_iguales, 2),
                porcentaje_reprobados=round(porcentaje_reprobados, 2),
            )
            
            # Congelar unidades temáticas
            for ut in self.curso.unidadtematica_set.all():
                UnidadTematicaCedula.objects.create(
                    cedula=self,
                    descripcion=ut.descripcion
                )
            
            # Congelar estrategias de enseñanza
            for ee in self.curso.estrategiaensenanza_set.all():
                EstrategiaEnsenanzaCedula.objects.create(
                    cedula=self,
                    descripcion=ee.descripcion
                )
            
            # Congelar estrategias de evaluación
            for ev in self.curso.estrategiaevaluacion_set.all():
                EstrategiaEvaluacionCedula.objects.create(
                    cedula=self,
                    descripcion=ev.descripcion
                )
            
            # Congelar prácticas
            for pr in self.curso.practica_set.all():
                PracticaCedula.objects.create(
                    cedula=self,
                    descripcion=pr.descripcion
                )
            
            # Congelar bibliografía
            for b in self.curso.bibliografia_set.all():
                BibliografiaCedula.objects.create(
                    cedula=self,
                    bibliografia=b,
                    referencia=str(b) # usa el __str__ del modelo original
                )
            
            # Congelar profesores actuales y de los últimos 2 años
            
            semestre_actual = self.periodo.semestre
            anio_actual = self.periodo.anio
            
            periodos_validos = []
            periodos_validos.append(self.periodo.nombre)  # periodo actual
            for i in range(1, 5):
                semestre_actual = "EM" if semestre_actual == "AD" else "AD"
                periodos_validos.append(f"{semestre_actual}{anio_actual}")
                if semestre_actual == "EM":
                    anio_actual -= 1
            
            profesores_curso = ProfesorCurso.objects.filter(
                curso=self.curso,
                periodo__nombre__in=periodos_validos
            )
            
            jerarquia = {
                'licenciatura': 1,
                'especialidad': 2,
                'maestria': 3,
                'doctorado': 4,
            }
            
            for pc in profesores_curso:
                profesor = pc.profesor
                
                # Buscar la formación más alta desde FormacionAcademica
                formaciones = profesor.formacionacademica_set.all()
                nombre_formacion = "No especificado"
                if formaciones.exists():
                    fm = max(formaciones, key=lambda f: jerarquia.get(f.nivel, 0))
                    nombre_formacion = fm.nombre
                
                # Determinar si tiene experiencia profesional
                experiencia = "Sí" if profesor.experienciaprofesional_set.exists() else "No"
                
                if pc.periodo_id == self.periodo_id:
                    # Profesor del periodo actual
                    ProfesorActualCedula.objects.create(
                        cedula=self,
                        profesor=profesor,
                        nombres=profesor.nombres,
                        apellidos=profesor.apellido_paterno + " " + profesor.apellido_materno,
                        formacion_nombre=nombre_formacion,
                        experiencia_profesional=experiencia,
                    )
                else:
                    # Profesor de años anteriores
                    ProfesorAnteriorCedula.objects.create(
                        cedula=self,
                        profesor=profesor,
                        nombres=profesor.nombres,
                        apellidos=profesor.apellido_paterno + " " + profesor.apellido_materno,
                        formacion_nombre=nombre_formacion,
                        experiencia_profesional=experiencia,
                    )

    def __str__(self):
        return f"Cédula {self.tipo} - {self.id}"

# ORGANIZACION CURRICULAR MODELS

class CursoObligatorio(models.Model):
    cedula = models.ForeignKey(Cedula, on_delete=models.PROTECT)
    curso = models.ForeignKey('core.Curso', on_delete=models.PROTECT)

class CursoOptativo(models.Model):
    cedula = models.ForeignKey(Cedula, on_delete=models.PROTECT)
    curso = models.ForeignKey('core.Curso', on_delete=models.PROTECT)

class CursoCurricular(models.Model):
    cedula = models.ForeignKey(Cedula, on_delete=models.PROTECT)
    curso = models.ForeignKey('core.Curso', on_delete=models.PROTECT)

class CursoObligatorioEje(models.Model):
    curso_obligatorio = models.ForeignKey(CursoObligatorio, on_delete=models.PROTECT)
    eje = models.ForeignKey("gestion_academica.EjeConocimiento", on_delete=models.PROTECT)
    nombre_eje = models.CharField(max_length=50)
    horas = models.PositiveIntegerField()

class CursoOptativoEje(models.Model):
    curso_optativo = models.ForeignKey(CursoOptativo, on_delete=models.PROTECT)
    eje = models.ForeignKey("gestion_academica.EjeConocimiento", on_delete=models.PROTECT)
    nombre_eje = models.CharField(max_length=50)
    horas = models.PositiveIntegerField()

class CursoCurricularEje(models.Model):
    curso_curricular = models.ForeignKey(CursoCurricular, on_delete=models.PROTECT)
    eje = models.ForeignKey("gestion_academica.EjeConocimiento", on_delete=models.PROTECT)
    nombre_eje = models.CharField(max_length=50)
    horas = models.PositiveIntegerField()

# CV SINTETICO MODELS

class ActualizacionDisciplinarCedula(models.Model):
    cedula = models.ForeignKey(Cedula, on_delete=models.PROTECT)
    actualizacion = models.ForeignKey('gestion_de_profesores.ActualizacionDisciplinar', on_delete=models.PROTECT)

class FormacionAcademicaCedula(models.Model):
    cedula = models.ForeignKey(Cedula, on_delete=models.PROTECT)
    formacion = models.ForeignKey('gestion_de_profesores.FormacionAcademica', on_delete=models.PROTECT)

class CapacitacionDocenteCedula(models.Model):
    cedula = models.ForeignKey(Cedula, on_delete=models.PROTECT)
    capacitacion = models.ForeignKey('gestion_de_profesores.CapacitacionDocente', on_delete=models.PROTECT)

class ExperienciaProfesionalCedula(models.Model):
    cedula = models.ForeignKey(Cedula, on_delete=models.PROTECT)
    experiencia = models.ForeignKey('gestion_de_profesores.ExperienciaProfesional', on_delete=models.PROTECT)

class ExperienciaDisenoCedula(models.Model):
    cedula = models.ForeignKey(Cedula, on_delete=models.PROTECT)
    experiencia = models.ForeignKey('gestion_de_profesores.ExperienciaDiseno', on_delete=models.PROTECT)

class LogroProfesionalCedula(models.Model):
    cedula = models.ForeignKey(Cedula, on_delete=models.PROTECT)
    logro = models.ForeignKey('gestion_de_profesores.LogroProfesional', on_delete=models.PROTECT)

class ParticipacionOrganizacionesCedula(models.Model):
    cedula = models.ForeignKey(Cedula, on_delete=models.PROTECT)
    participacion = models.ForeignKey('gestion_de_profesores.ParticipacionOrganizaciones', on_delete=models.PROTECT)

class PremioDistincionCedula(models.Model):
    cedula = models.ForeignKey(Cedula, on_delete=models.PROTECT)
    premio = models.ForeignKey('gestion_de_profesores.PremioDistincion', on_delete=models.PROTECT)

class ProductoAcademicoCedula(models.Model):
    cedula = models.ForeignKey(Cedula, on_delete=models.PROTECT)
    producto = models.ForeignKey('gestion_de_profesores.ProductoAcademico', on_delete=models.PROTECT)

class AportacionPECedula(models.Model):
    cedula = models.ForeignKey(Cedula, on_delete=models.PROTECT)
    aportacion = models.ForeignKey('evaluacion_acreditacion.AportacionPE', on_delete=models.PROTECT)

class GestionAcademicaCedula(models.Model):
    cedula = models.ForeignKey(Cedula, on_delete=models.PROTECT)
    gestion = models.ForeignKey('evaluacion_acreditacion.GestionAcademica', on_delete=models.PROTECT)

# PLAN DE MEJORA MODELS

class HallazgoCedula(models.Model):
    cedula = models.ForeignKey(Cedula, on_delete=models.PROTECT)
    hallazgo = models.ForeignKey('evaluacion_acreditacion.Hallazgo', on_delete=models.PROTECT)

class AccionMejoraCedula(models.Model):
    cedula = models.ForeignKey(Cedula, on_delete=models.PROTECT)
    hallazgo = models.ForeignKey('evaluacion_acreditacion.Hallazgo', on_delete=models.PROTECT)
    accion = models.ForeignKey('evaluacion_acreditacion.AccionMejora', on_delete=models.PROTECT)

# VALORACION DE OBJETIVOS MODELS

class ObjetivoEducacionalCedula(models.Model):
    cedula = models.ForeignKey(Cedula, on_delete=models.PROTECT)
    objetivo = models.ForeignKey('gestion_academica.ObjetivoEducacional', on_delete=models.PROTECT)

class AtributoObjetivoCedula(models.Model):
    cedula = models.ForeignKey(Cedula, on_delete=models.PROTECT)
    objetivo = models.ForeignKey('gestion_academica.ObjetivoEducacional', on_delete=models.PROTECT)
    atributo = models.ForeignKey('gestion_academica.AtributoPE', on_delete=models.PROTECT)

class CriterioDesempenoCedula(models.Model):
    cedula = models.ForeignKey(Cedula, on_delete=models.PROTECT)
    atributo = models.ForeignKey('gestion_academica.AtributoPE', on_delete=models.PROTECT)
    criterio = models.ForeignKey('gestion_academica.CriterioDesempeno', on_delete=models.PROTECT)


class IndicadorCedula(models.Model):
    cedula = models.ForeignKey(Cedula, on_delete=models.PROTECT)
    criterio = models.ForeignKey('gestion_academica.CriterioDesempeno', on_delete=models.PROTECT)
    indicador = models.ForeignKey('evaluacion_acreditacion.Indicador', on_delete=models.PROTECT)

class EvaluacionIndicadorCedula(models.Model):
    cedula = models.ForeignKey(Cedula, on_delete=models.PROTECT)
    indicador = models.ForeignKey('evaluacion_acreditacion.Indicador', on_delete=models.PROTECT)
    evaluacion = models.ForeignKey('evaluacion_acreditacion.EvaluacionIndicador', on_delete=models.PROTECT)

# AEP vs AE-CACEI MODELS

class AtributoPECedula(models.Model):
    cedula = models.ForeignKey(Cedula, on_delete=models.PROTECT)
    atributo_pe = models.ForeignKey('gestion_academica.AtributoPE', on_delete=models.PROTECT)

class AtributoPECACEICedula(models.Model):
    cedula = models.ForeignKey(Cedula, on_delete=models.PROTECT)
    atributo_pe = models.ForeignKey('gestion_academica.AtributoPE', on_delete=models.PROTECT)
    atributo_cacei = models.ForeignKey('gestion_academica.AtributoCACEI', on_delete=models.PROTECT)
    relacion = models.ForeignKey('gestion_academica.AtributoPECACEI', on_delete=models.PROTECT)

# AEP vs OE MODELS

class AtributoObjetivoCedulaAEPVsOE(models.Model):
    cedula = models.ForeignKey(Cedula, on_delete=models.PROTECT)
    objetivo = models.ForeignKey('gestion_academica.ObjetivoEducacional', on_delete=models.PROTECT)
    atributo_pe = models.ForeignKey('gestion_academica.AtributoPE', on_delete=models.PROTECT)
    relacion = models.ForeignKey('gestion_academica.AtributoPEObjetivo', on_delete=models.PROTECT)

# CURSOS vs AEP MODELS

class CursoCedula(models.Model):
    cedula = models.ForeignKey(Cedula, on_delete=models.PROTECT)
    curso = models.ForeignKey('core.Curso', on_delete=models.PROTECT)

class CursoAtributoPECedula(models.Model):
    cedula = models.ForeignKey(Cedula, on_delete=models.PROTECT)
    curso = models.ForeignKey('core.Curso', on_delete=models.PROTECT)
    atributo_pe = models.ForeignKey('gestion_academica.AtributoPE', on_delete=models.PROTECT)
    relacion = models.ForeignKey('gestion_academica.CursoAtributoPE', on_delete=models.PROTECT)
    nombre_abreviado = models.CharField(max_length=50)
    nivel_aporte = models.CharField(max_length=1)

# PROGRAMA DE ASIGNATURA MODELS

class CursoInfoCedula(models.Model):
    cedula = models.ForeignKey(Cedula, on_delete=models.PROTECT)
    clave = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    seriacion = models.TextField(blank=True, null=True)
    ubicacion = models.CharField(max_length=50)
    tipo = models.CharField(max_length=50)
    objetivo_general = models.TextField(blank=True, null=True)
    numero_grupos = models.PositiveSmallIntegerField()

class CursoEjeCedula(models.Model):
    cedula = models.ForeignKey(Cedula, on_delete=models.PROTECT)
    eje = models.ForeignKey('gestion_academica.EjeConocimiento', on_delete=models.PROTECT)
    nombre_eje = models.CharField(max_length=50)
    horas = models.PositiveIntegerField()

class CursoObjetivoEspecificoCedula(models.Model):
    cedula = models.ForeignKey(Cedula, on_delete=models.PROTECT)
    objetivo = models.ForeignKey('gestion_academica.ObjetivoEspecifico', on_delete=models.PROTECT)
    descripcion = models.TextField(blank=True, null=True)

class HorasSemanaCedula(models.Model):
    cedula = models.ForeignKey(Cedula, on_delete=models.PROTECT)
    horas_totales = models.PositiveSmallIntegerField()
    horas_aula = models.PositiveSmallIntegerField()
    horas_laboratorio = models.PositiveSmallIntegerField()
    horas_practicas = models.PositiveSmallIntegerField()

class CursoEstadisticasCedula(models.Model):
    cedula = models.ForeignKey(Cedula, on_delete=models.PROTECT)
    promedio = models.FloatField()
    porcentaje_mayores_iguales = models.FloatField()
    porcentaje_reprobados = models.FloatField()

class UnidadTematicaCedula(models.Model):
    cedula = models.ForeignKey(Cedula, on_delete=models.PROTECT)
    descripcion = models.TextField(blank=True, null=True)

class EstrategiaEnsenanzaCedula(models.Model):
    cedula = models.ForeignKey(Cedula, on_delete=models.PROTECT)
    descripcion = models.TextField(blank=True, null=True)

class EstrategiaEvaluacionCedula(models.Model):
    cedula = models.ForeignKey(Cedula, on_delete=models.PROTECT)
    descripcion = models.TextField(blank=True, null=True)

class PracticaCedula(models.Model):
    cedula = models.ForeignKey(Cedula, on_delete=models.PROTECT)
    descripcion = models.TextField(blank=True, null=True)

class BibliografiaCedula(models.Model):
    cedula = models.ForeignKey(Cedula, on_delete=models.PROTECT)
    bibliografia = models.ForeignKey('gestion_academica.Bibliografia', on_delete=models.PROTECT)
    referencia = models.TextField()

class ProfesorActualCedula(models.Model):
    cedula = models.ForeignKey(Cedula, on_delete=models.PROTECT)
    profesor = models.ForeignKey('core.Profesor', on_delete=models.PROTECT)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    formacion_nombre = models.CharField(max_length=100)
    experiencia_profesional = models.BooleanField(default=False)

class ProfesorAnteriorCedula(models.Model):
    cedula = models.ForeignKey(Cedula, on_delete=models.PROTECT)
    profesor = models.ForeignKey('core.Profesor', on_delete=models.PROTECT)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    formacion_nombre = models.CharField(max_length=100)
    experiencia_profesional = models.CharField(max_length=2)
```
###serializers.py
<p>
Esta clase sirve para consultar y actualizar la base de datos.
</p>

```python
from rest_framework import serializers

from django.db.models import Sum

from gestion_academica.serializers import AtributoCACEISerializer, AtributoPECACEISerializer, AtributoPEObjetivoSerializer, AtributoPESerializer, CriterioDesempenoSerializer, CursoAtributoPESerializer, ObjetivoEducacionalSerializer
from cedulas.models import AccionMejoraCedula, ActualizacionDisciplinarCedula, AportacionPECedula, AtributoObjetivoCedula, AtributoObjetivoCedulaAEPVsOE, AtributoPECACEICedula, AtributoPECedula, BibliografiaCedula, CapacitacionDocenteCedula, Cedula, CriterioDesempenoCedula, CursoAtributoPECedula, CursoCedula, CursoCurricular, CursoCurricularEje, CursoEjeCedula, CursoEstadisticasCedula, CursoInfoCedula, CursoObjetivoEspecificoCedula, CursoObligatorio, CursoObligatorioEje, CursoOptativo, CursoOptativoEje, EstrategiaEnsenanzaCedula, EstrategiaEvaluacionCedula, EvaluacionIndicadorCedula, ExperienciaDisenoCedula, ExperienciaProfesionalCedula, FormacionAcademicaCedula, GestionAcademicaCedula, HallazgoCedula, HorasSemanaCedula, IndicadorCedula, LogroProfesionalCedula, ObjetivoEducacionalCedula, ParticipacionOrganizacionesCedula, PracticaCedula, PremioDistincionCedula, ProductoAcademicoCedula, ProfesorActualCedula, ProfesorAnteriorCedula, UnidadTematicaCedula
from core.models import Curso, Periodo, Profesor, ProgramaEducativo

from gestion_de_profesores.serializers import ActualizacionDisciplinarSerializer, CapacitacionDocenteSerializer, ExperienciaDisenoSerializer, ExperienciaProfesionalSerializer, FormacionAcademicaSerializer, LogroProfesionalSerializer, ParticipacionOrganizacionesSerializer, PremioDistincionSerializer, ProductoAcademicoSerializer
from core.serializers import CursoSerializer, PeriodoSerializer, ProgramaEducativoSerializer, ProfesorSerializer
from evaluacion_acreditacion.serializers import AccionMejoraSerializer, AportacionPESerializer, EvaluacionIndicadorSerializer, GestionAcademicaSerializer, HallazgoSerializer, IndicadorSerializer

class CedulaOrganizacionCurricularSerializer(serializers.ModelSerializer):
    programa = ProgramaEducativoSerializer(read_only=True)
    periodo = PeriodoSerializer(read_only=True)
    programa_id = serializers.PrimaryKeyRelatedField(
        queryset=ProgramaEducativo.objects.all(), source='programa', write_only=True
    )
    periodo_id = serializers.PrimaryKeyRelatedField(
        queryset=Periodo.objects.all(), source='periodo', write_only=True
    )

    cursos_obligatorios = serializers.SerializerMethodField()
    cursos_optativos = serializers.SerializerMethodField()
    cursos_curriculares = serializers.SerializerMethodField()
    resumen_horas_cursos_obligatorios = serializers.SerializerMethodField()
    resumen_horas_cursos_optativos = serializers.SerializerMethodField()
    resumen_combinado = serializers.SerializerMethodField()

    class Meta:
        model = Cedula
        fields = [
            "id", "programa", "programa_id", "periodo", "periodo_id", "tipo",
            "cursos_obligatorios",
            "cursos_optativos",
            "cursos_curriculares",
            "resumen_horas_cursos_obligatorios",
            "resumen_horas_cursos_optativos",
            "resumen_combinado"
        ]
        read_only_fields = ["id"]
    
    def get_cursos_obligatorios(self, obj):
        relaciones = CursoObligatorio.objects.filter(cedula=obj)
        return CursoObligatorioSerializer(relaciones, many=True).data

    def get_cursos_optativos(self, obj):
        relaciones = CursoOptativo.objects.filter(cedula=obj)
        return CursoOptativoSerializer(relaciones, many=True).data
    
    def get_cursos_curriculares(self, obj):
        relaciones = CursoCurricular.objects.filter(cedula=obj)
        return CursoCurricularSerializer(relaciones, many=True).data

    def get_resumen_horas_cursos_obligatorios(self, obj):
        resumen = CursoObligatorioEje.objects.filter(
            curso_obligatorio__cedula=obj
        ).values('nombre_eje').annotate(total_horas=Sum('horas'))
        
        total = sum(r['total_horas'] for r in resumen)
        
        return {
            "por_eje": resumen,
            "total_general": total
        }

    def get_resumen_horas_cursos_optativos(self, obj):
        resumen = CursoOptativoEje.objects.filter(
            curso_optativo__cedula=obj
        ).values('nombre_eje').annotate(total_horas=Sum('horas'))
        
        total = sum(r['total_horas'] for r in resumen)
        
        return {
            "por_eje": resumen,
            "total_general": total
        }

    def get_resumen_combinado(self, obj):
        from collections import defaultdict
        
        # Obtener ejes obligatorios
        obligatorios = CursoObligatorioEje.objects.filter(
            curso_obligatorio__cedula=obj
        ).values('nombre_eje').annotate(total_horas=Sum('horas'))
        
        # Obtener ejes optativos
        optativos = CursoOptativoEje.objects.filter(
            curso_optativo__cedula=obj
        ).values('nombre_eje').annotate(total_horas=Sum('horas'))
        
        # Combinar por nombre_eje
        resumen = defaultdict(int)
        for r in obligatorios:
            resumen[r['nombre_eje']] += r['total_horas']
        for r in optativos:
            resumen[r['nombre_eje']] += r['total_horas']
        
        total_general = sum(resumen.values())
        
        por_eje = []
        for nombre_eje, total_horas in resumen.items():
            porcentaje = (total_horas / total_general * 100) if total_general > 0 else 0
            por_eje.append({
                'nombre_eje': nombre_eje,
                'total_horas': total_horas,
                'porcentaje': "{:.2f}".format(porcentaje)
            })
        
        return {
            "por_eje": por_eje,
            "total_general": total_general
        }

class CursoObligatorioEjeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CursoObligatorioEje
        fields = ["id", "nombre_eje", "horas"]

class CursoOptativoEjeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CursoOptativoEje
        fields = ["id", "nombre_eje", "horas"]

class CursoCurricularEjeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CursoCurricularEje
        fields = ["id", "nombre_eje", "horas"]

class CursoOptativoSerializer(serializers.ModelSerializer):
    curso_clave = serializers.CharField(source='curso.clave', read_only=True)
    curso_nombre = serializers.CharField(source='curso.nombre', read_only=True)
    ejes = CursoOptativoEjeSerializer(many=True, read_only=True, source='cursooptativoeje_set')
    
    class Meta:
        model = CursoOptativo
        fields = ["id", "curso_clave", "curso_nombre", "ejes"]

class CursoObligatorioSerializer(serializers.ModelSerializer):
    curso_clave = serializers.CharField(source='curso.clave', read_only=True)
    curso_nombre = serializers.CharField(source='curso.nombre', read_only=True)
    ejes = CursoObligatorioEjeSerializer(many=True, read_only=True, source='cursoobligatorioeje_set')
    
    class Meta:
        model = CursoObligatorio
        fields = ["id", "curso_clave", "curso_nombre", "ejes"]

class CursoCurricularSerializer(serializers.ModelSerializer):
    curso_clave = serializers.CharField(source='curso.clave', read_only=True)
    curso_nombre = serializers.CharField(source='curso.nombre', read_only=True)
    ejes = CursoCurricularEjeSerializer(many=True, read_only=True, source='cursocurriculareje_set')
    
    class Meta:
        model = CursoCurricular
        fields = ["id", "curso_clave", "curso_nombre", "ejes"]

class CedulaCvSinteticoSerializer(serializers.ModelSerializer):
    profesor = ProfesorSerializer(read_only=True)
    profesor_id = serializers.PrimaryKeyRelatedField(
        queryset=Profesor.objects.all(), source='profesor', write_only=True
    )
    periodo = PeriodoSerializer(read_only=True)
    periodo_id = serializers.PrimaryKeyRelatedField(
        queryset=Periodo.objects.all(), source='periodo', write_only=True
    )
    
    actualizaciones = ActualizacionDisciplinarSerializer(many=True, read_only=True)
    formaciones = serializers.SerializerMethodField()
    capacitaciones = serializers.SerializerMethodField()
    experiencias = serializers.SerializerMethodField()
    disenos = serializers.SerializerMethodField()
    logros = serializers.SerializerMethodField()
    participaciones = serializers.SerializerMethodField()
    premios = serializers.SerializerMethodField()
    productos = serializers.SerializerMethodField()
    aportaciones_pe = serializers.SerializerMethodField()
    gestiones = serializers.SerializerMethodField()

    class Meta:
        model = Cedula
        fields = [
            "id", "tipo", "profesor", "profesor_id", "periodo", "periodo_id",
            "actualizaciones", "formaciones", "capacitaciones", "experiencias", 
            "disenos", "logros", "participaciones", "premios", "productos", 
            "aportaciones_pe", "gestiones"
        ]
        read_only_fields = ["id"]
    
    def get_actualizaciones(self, obj):
        relaciones = ActualizacionDisciplinarCedula.objects.filter(cedula=obj)
        return ActualizacionDisciplinarCedulaSerializer(relaciones, many=True).data
    
    def get_formaciones(self, obj):
        relaciones = FormacionAcademicaCedula.objects.filter(cedula=obj)
        return FormacionAcademicaCedulaSerializer(relaciones, many=True).data
    
    def get_capacitaciones(self, obj):
        relaciones = CapacitacionDocenteCedula.objects.filter(cedula=obj)
        return CapacitacionDocenteCedulaSerializer(relaciones, many=True).data
    
    def get_experiencias(self, obj):
        relaciones = ExperienciaProfesionalCedula.objects.filter(cedula=obj)
        return ExperienciaProfesionalCedulaSerializer(relaciones, many=True).data
    
    def get_disenos(self, obj):
        relaciones = ExperienciaDisenoCedula.objects.filter(cedula=obj)
        return ExperienciaDisenoCedulaSerializer(relaciones, many=True).data
    
    def get_logros(self, obj):   
        relaciones = LogroProfesionalCedula.objects.filter(cedula=obj)
        return LogroProfesionalCedulaSerializer(relaciones, many=True).data
    
    def get_participaciones(self, obj):
        relaciones = ParticipacionOrganizacionesCedula.objects.filter(cedula=obj)
        return ParticipacionOrganizacionesCedulaSerializer(relaciones, many=True).data
    
    def get_premios(self, obj):
        relaciones = PremioDistincionCedula.objects.filter(cedula=obj)
        return PremioDistincionCedulaSerializer(relaciones, many=True).data
    
    def get_productos(self, obj):
        relaciones = ProductoAcademicoCedula.objects.filter(cedula=obj)
        return ProductoAcademicoCedulaSerializer(relaciones, many=True).data
    
    def get_aportaciones_pe(self, obj):
        relaciones = AportacionPECedula.objects.filter(cedula=obj)
        return AportacionPECedulaSerializer(relaciones, many=True).data
    
    def get_gestiones(self, obj):
        relaciones = GestionAcademicaCedula.objects.filter(cedula=obj)
        return GestionAcademicaCedulaSerializer(relaciones, many=True).data

class ActualizacionDisciplinarCedulaSerializer(serializers.ModelSerializer):
    actualizacion = ActualizacionDisciplinarSerializer(read_only=True)

    class Meta:
        model = ActualizacionDisciplinarCedula
        fields = ["id", "actualizacion"]

class FormacionAcademicaCedulaSerializer(serializers.ModelSerializer):
    formacion = FormacionAcademicaSerializer(read_only=True)

    class Meta:
        model = FormacionAcademicaCedula
        fields = ["id", "formacion"]

class CapacitacionDocenteCedulaSerializer(serializers.ModelSerializer):
    capacitacion = CapacitacionDocenteSerializer(read_only=True)

    class Meta:
        model = CapacitacionDocenteCedula
        fields = ["id", "capacitacion"]

class ExperienciaProfesionalCedulaSerializer(serializers.ModelSerializer):
    experiencia = ExperienciaProfesionalSerializer(read_only=True)

    class Meta:
        model = ExperienciaProfesionalCedula
        fields = ["id", "experiencia"]

class ExperienciaDisenoCedulaSerializer(serializers.ModelSerializer):
    experiencia = ExperienciaDisenoSerializer(read_only=True)

    class Meta:
        model = ExperienciaDisenoCedula
        fields = ["id", "experiencia"]

class LogroProfesionalCedulaSerializer(serializers.ModelSerializer):
    logro = LogroProfesionalSerializer(read_only=True)

    class Meta:
        model = LogroProfesionalCedula
        fields = ["id", "logro"]

class ParticipacionOrganizacionesCedulaSerializer(serializers.ModelSerializer):
    participacion = ParticipacionOrganizacionesSerializer(read_only=True)

    class Meta:
        model = ParticipacionOrganizacionesCedula
        fields = ["id", "participacion"]

class PremioDistincionCedulaSerializer(serializers.ModelSerializer):
    premio = PremioDistincionSerializer(read_only=True)

    class Meta:
        model = PremioDistincionCedula
        fields = ["id", "premio"]

class ProductoAcademicoCedulaSerializer(serializers.ModelSerializer):
    producto = ProductoAcademicoSerializer(read_only=True)

    class Meta:
        model = ProductoAcademicoCedula
        fields = ["id", "producto"]

class AportacionPECedulaSerializer(serializers.ModelSerializer):
    aportacion = AportacionPESerializer(read_only=True)

    class Meta:
        model = AportacionPECedula
        fields = ["id", "aportacion"]

class GestionAcademicaCedulaSerializer(serializers.ModelSerializer):
    gestion = GestionAcademicaSerializer(read_only=True)

    class Meta:
        model = GestionAcademicaCedula
        fields = ["id", "gestion"]

class CedulaPlanMejoraSerializer(serializers.ModelSerializer):
    programa = ProgramaEducativoSerializer(read_only=True)
    periodo = PeriodoSerializer(read_only=True)
    programa_id = serializers.PrimaryKeyRelatedField(
        queryset=ProgramaEducativo.objects.all(), source='programa', write_only=True
    )
    periodo_id = serializers.PrimaryKeyRelatedField(
        queryset=Periodo.objects.all(), source='periodo', write_only=True
    )
    hallazgos = serializers.SerializerMethodField()

    class Meta:
        model = Cedula
        fields = [
            "id", "tipo", "programa", "periodo", "programa_id", "periodo_id",
            "hallazgos"
        ]
        read_only_fields = ["id"]
    
    def get_hallazgos(self, obj):
        relaciones = HallazgoCedula.objects.filter(cedula=obj)
        return HallazgoCedulaSerializer(relaciones, many=True).data

class HallazgoCedulaSerializer(serializers.ModelSerializer):
    hallazgo = HallazgoSerializer(read_only=True)

    class Meta:
        model = HallazgoCedula
        fields = ["id", "hallazgo"]

class AccionMejoraCedulaSerializer(serializers.ModelSerializer):
    accion = AccionMejoraSerializer(read_only=True)
    
    class Meta:
        model = AccionMejoraCedula
        fields = ["id", "accion"]

class CedulaValoracionObjetivosSerializer(serializers.ModelSerializer):
    programa = ProgramaEducativoSerializer(read_only=True)
    periodo = PeriodoSerializer(read_only=True)
    programa_id = serializers.PrimaryKeyRelatedField(
        queryset=ProgramaEducativo.objects.all(), source='programa', write_only=True
    )
    periodo_id = serializers.PrimaryKeyRelatedField(
        queryset=Periodo.objects.all(), source='periodo', write_only=True
    )
    objetivos = serializers.SerializerMethodField()
    
    class Meta:
        model = Cedula
        fields = ["id", "tipo", "programa", "periodo", "programa_id", "periodo_id", "objetivos"]
        read_only_fields = ["id"]
    
    def get_objetivos(self, obj):
        relaciones = ObjetivoEducacionalCedula.objects.filter(cedula=obj)
        return ObjetivoEducacionalCedulaSerializer(relaciones, many=True).data

class EvaluacionIndicadorCedulaSerializer(serializers.ModelSerializer):
    evaluacion = EvaluacionIndicadorSerializer(read_only=True)
    curso = serializers.SerializerMethodField()
    
    class Meta:
        model = EvaluacionIndicadorCedula
        fields = ["id", "evaluacion", "curso"]
    
    def get_curso(self, obj):
        if self.context.get("include_curso", False):
            if obj.evaluacion and obj.evaluacion.curso:
                return CursoSerializer(obj.evaluacion.curso).data
        return None

class IndicadorCedulaSerializer(serializers.ModelSerializer):
    indicador = IndicadorSerializer(read_only=True)
    evaluaciones = serializers.SerializerMethodField()
    
    class Meta:
        model = IndicadorCedula
        fields = ["id", "indicador", "evaluaciones"]
        
    def get_evaluaciones(self, obj):
        relaciones = EvaluacionIndicadorCedula.objects.filter(cedula=obj.cedula, indicador=obj.indicador)
        return EvaluacionIndicadorCedulaSerializer(relaciones, many=True, context=self.context).data

class CriterioCedulaSerializer(serializers.ModelSerializer):
    criterio = CriterioDesempenoSerializer(read_only=True)
    indicadores = serializers.SerializerMethodField()
    
    class Meta:
        model = CriterioDesempenoCedula
        fields = ["id", "criterio", "indicadores"]

    def get_indicadores(self, obj):
        relaciones = IndicadorCedula.objects.filter(cedula=obj.cedula, criterio=obj.criterio)
        return IndicadorCedulaSerializer(relaciones, many=True, context=self.context).data

class AtributoObjetivoCedulaSerializer(serializers.ModelSerializer):
    atributo = AtributoPESerializer(read_only=True)
    criterios = serializers.SerializerMethodField()
    
    class Meta:
        model = AtributoObjetivoCedula
        fields = ["id", "atributo", "criterios"]
    
    def get_criterios(self, obj):
        relaciones = CriterioDesempenoCedula.objects.filter(cedula=obj.cedula, atributo=obj.atributo)
        return CriterioCedulaSerializer(relaciones, many=True, context=self.context).data

class ObjetivoEducacionalCedulaSerializer(serializers.ModelSerializer):
    objetivo = ObjetivoEducacionalSerializer(read_only=True)
    atributos = serializers.SerializerMethodField()
    
    class Meta:
        model = ObjetivoEducacionalCedula
        fields = ["id", "objetivo", "atributos"]
    
    def get_atributos(self, obj):
        relaciones = AtributoObjetivoCedula.objects.filter(cedula=obj.cedula, objetivo=obj.objetivo)
        return AtributoObjetivoCedulaSerializer(relaciones, many=True).data

class CedulaAEPVsAECACEISerializer(serializers.ModelSerializer):
    programa = ProgramaEducativoSerializer(read_only=True)
    periodo = PeriodoSerializer(read_only=True)
    programa_id = serializers.PrimaryKeyRelatedField(
        queryset=ProgramaEducativo.objects.all(), source='programa', write_only=True
    )
    periodo_id = serializers.PrimaryKeyRelatedField(
        queryset=Periodo.objects.all(), source='periodo', write_only=True
    )
    atributos_pe = serializers.SerializerMethodField()
    
    class Meta:
        model = Cedula
        fields = ["id", "tipo", "programa", "programa_id", "periodo", "periodo_id", "atributos_pe"]
    
    def get_atributos_pe(self, obj):
        relaciones = AtributoPECedula.objects.filter(cedula=obj)
        return AtributoPECedulaSerializer(relaciones, many=True).data

class AtributoPECACEICedulaSerializer(serializers.ModelSerializer):
    atributo_pe = AtributoPESerializer(read_only=True)
    atributo_cacei = AtributoCACEISerializer(read_only=True)
    relacion = AtributoPECACEISerializer(read_only=True)
    
    class Meta:
        model = AtributoPECACEICedula
        fields = ["id", "atributo_pe", "atributo_cacei", "relacion"]

class AtributoPECedulaSerializer(serializers.ModelSerializer):
    atributo_pe = AtributoPESerializer(read_only=True)
    relaciones_cacei = serializers.SerializerMethodField()
    
    class Meta:
        model = AtributoPECedula
        fields = ["id", "atributo_pe", "relaciones_cacei"]
    
    def get_relaciones_cacei(self, obj):
        relaciones = AtributoPECACEICedula.objects.filter(cedula=obj.cedula, atributo_pe=obj.atributo_pe)
        return AtributoPECACEICedulaSerializer(relaciones, many=True).data

class CedulaAEPVsOESerializer(serializers.ModelSerializer):
    programa = ProgramaEducativoSerializer(read_only=True)
    periodo = PeriodoSerializer(read_only=True)
    programa_id = serializers.PrimaryKeyRelatedField(
        queryset=ProgramaEducativo.objects.all(), source='programa', write_only=True
    )
    periodo_id = serializers.PrimaryKeyRelatedField(
        queryset=Periodo.objects.all(), source='periodo', write_only=True
    )
    atributos_pe = serializers.SerializerMethodField()
    
    class Meta:
        model = Cedula
        fields = ["id", "tipo", "programa", "programa_id", "periodo", "periodo_id", "atributos_pe"]
    
    def get_atributos_pe(self, obj):
        relaciones = AtributoPECedula.objects.filter(cedula=obj)
        return AtributoPECedulaAEPVsOESerializer(relaciones, many=True).data

class AtributoObjetivoCedulaAEPVsOESerializer(serializers.ModelSerializer):
    atributo_pe = AtributoPESerializer(read_only=True)
    objetivo = ObjetivoEducacionalSerializer(read_only=True)
    relacion = AtributoPEObjetivoSerializer(read_only=True)
    
    class Meta:
        model = AtributoObjetivoCedulaAEPVsOE
        fields = ["id", "atributo_pe", "objetivo", "relacion"]

class AtributoPECedulaAEPVsOESerializer(serializers.ModelSerializer):
    atributo_pe = AtributoPESerializer(read_only=True)
    objetivos = serializers.SerializerMethodField()
    
    class Meta:
        model = AtributoPECedula
        fields = ["id", "atributo_pe", "objetivos"]
    
    def get_objetivos(self, obj):
        relaciones = AtributoObjetivoCedulaAEPVsOE.objects.filter(
            cedula=obj.cedula, atributo_pe=obj.atributo_pe
        )
        return AtributoObjetivoCedulaAEPVsOESerializer(relaciones, many=True).data

class CedulaCursosVsAEPSerializer(serializers.ModelSerializer):
    programa = ProgramaEducativoSerializer(read_only=True)
    periodo = PeriodoSerializer(read_only=True)
    programa_id = serializers.PrimaryKeyRelatedField(
        queryset=ProgramaEducativo.objects.all(), source='programa', write_only=True
    )
    periodo_id = serializers.PrimaryKeyRelatedField(
        queryset=Periodo.objects.all(), source='periodo', write_only=True
    )
    cursos = serializers.SerializerMethodField()
    
    class Meta:
        model = Cedula
        fields = ["id", "tipo", "programa", "programa_id", "periodo", "periodo_id", "cursos"]
    
    def get_cursos(self, obj):
        relaciones = CursoCedula.objects.filter(cedula=obj)
        return CursoCedulaSerializer(relaciones, many=True).data

class CursoCedulaSerializer(serializers.ModelSerializer):
    curso = CursoSerializer(read_only=True)
    atributos_pe = serializers.SerializerMethodField()
    
    class Meta:
        model = CursoCedula
        fields = ["id", "curso", "atributos_pe"]
    
    def get_atributos_pe(self, obj):
        relaciones = CursoAtributoPECedula.objects.filter(
            cedula=obj.cedula, curso=obj.curso
        )
        return CursoAtributoPECedulaSerializer(relaciones, many=True).data

class CursoAtributoPECedulaSerializer(serializers.ModelSerializer):
    curso = CursoSerializer(read_only=True)
    atributo_pe = AtributoPESerializer(read_only=True)
    relacion = CursoAtributoPESerializer(read_only=True)
    
    class Meta:
        model = CursoAtributoPECedula
        fields = ["id", "curso", "atributo_pe", "relacion", "nombre_abreviado", "nivel_aporte"]

class AtributoPECedulaHerramientasSerializer(serializers.ModelSerializer):
    atributo_pe = AtributoPESerializer(read_only=True)
    criterios = serializers.SerializerMethodField()
    
    class Meta:
        model = AtributoPECedula
        fields = ["id", "atributo_pe", "criterios"]
    
    def get_criterios(self, obj):
        relaciones = CriterioDesempenoCedula.objects.filter(
            cedula=obj.cedula, atributo_pe=obj.atributo_pe
        )
        return CriterioCedulaSerializer(relaciones, many=True, context=self.context).data

class CedulaHerramientasValoracionAEPSerializer(serializers.ModelSerializer):
    programa = ProgramaEducativoSerializer(read_only=True)
    periodo = PeriodoSerializer(read_only=True)
    programa_id = serializers.PrimaryKeyRelatedField(
        queryset=ProgramaEducativo.objects.all(), source='programa', write_only=True
    )
    periodo_id = serializers.PrimaryKeyRelatedField(
        queryset=Periodo.objects.all(), source='periodo', write_only=True
    )
    atributos_pe = serializers.SerializerMethodField()
    
    class Meta:
        model = Cedula
        fields = ["id", "tipo", "programa", "programa_id", "periodo", "periodo_id", "atributos_pe"]
    
    def get_atributos_pe(self, obj):
        relaciones = AtributoPECedula.objects.filter(cedula=obj)
        return AtributoPECedulaHerramientasSerializer(relaciones, many=True).data

class CedulaProgramaAsignaturaSerializer(serializers.ModelSerializer):
    programa = ProgramaEducativoSerializer(read_only=True)
    periodo = PeriodoSerializer(read_only=True)
    curso = CursoSerializer(read_only=True)
    programa_id = serializers.PrimaryKeyRelatedField(
        queryset=ProgramaEducativo.objects.all(), source='programa', write_only=True
    )
    periodo_id = serializers.PrimaryKeyRelatedField(
        queryset=Periodo.objects.all(), source='periodo', write_only=True
    )
    curso_id = serializers.PrimaryKeyRelatedField(
        queryset=Curso.objects.all(), source='curso', write_only=True
    )
    
    curso_info = serializers.SerializerMethodField()
    ejes = serializers.SerializerMethodField()
    objetivos = serializers.SerializerMethodField()
    atributos_pe = serializers.SerializerMethodField()
    horas_semana = serializers.SerializerMethodField()
    estadisticas = serializers.SerializerMethodField()
    unidades_tematicas = serializers.SerializerMethodField()
    estrategias_ensenanza = serializers.SerializerMethodField()
    estrategias_evaluacion = serializers.SerializerMethodField()
    practicas = serializers.SerializerMethodField()
    bibliografia = serializers.SerializerMethodField()
    profesores_actuales = serializers.SerializerMethodField()
    profesores_anteriores = serializers.SerializerMethodField()
    
    class Meta:
        model = Cedula
        fields = [
            "id", "tipo", "programa", "programa_id", "periodo", "periodo_id", "curso", "curso_id",
            "curso_info", "ejes", "objetivos", "atributos_pe", "horas_semana", 
            "estadisticas", "unidades_tematicas", "estrategias_ensenanza", 
            "estrategias_evaluacion", "practicas", "bibliografia",
            "profesores_actuales", "profesores_anteriores"
        ]
    
    def get_curso_info(self, obj):
        relaciones = CursoInfoCedula.objects.filter(cedula=obj)
        return CursoInfoCedulaSerializer(relaciones, many=True).data
    
    def get_ejes(self, obj):
        relaciones = CursoEjeCedula.objects.filter(cedula=obj)
        return CursoEjeCedulaSerializer(relaciones, many=True).data
    
    def get_objetivos(self, obj):
        relaciones = CursoObjetivoEspecificoCedula.objects.filter(cedula=obj)
        return CursoObjetivoEspecificoCedulaSerializer(relaciones, many=True).data
    
    def get_atributos_pe(self, obj):
        relaciones = CursoAtributoPECedula.objects.filter(cedula=obj)
        return CursoAtributoPECedulaSerializer(relaciones, many=True).data
    
    def get_horas_semana(self, obj):
        relaciones = HorasSemanaCedula.objects.filter(cedula=obj)
        return HorasSemanaCedulaSerializer(relaciones, many=True).data
    
    def get_estadisticas(self, obj):
        relaciones = CursoEstadisticasCedula.objects.filter(cedula=obj)
        return CursoEstadisticasCedulaSerializer(relaciones, many=True).data
    
    def get_unidades_tematicas(self, obj):
        relaciones = UnidadTematicaCedula.objects.filter(cedula=obj)
        return UnidadTematicaCedulaSerializer(relaciones, many=True).data
    
    def get_estrategias_ensenanza(self, obj):
        relaciones = EstrategiaEnsenanzaCedula.objects.filter(cedula=obj)
        return EstrategiaEnsenanzaCedulaSerializer(relaciones, many=True).data
    
    def get_estrategias_evaluacion(self, obj):
        relaciones = EstrategiaEvaluacionCedula.objects.filter(cedula=obj)
        return EstrategiaEvaluacionCedulaSerializer(relaciones, many=True).data
    
    def get_practicas(self, obj):
        relaciones = PracticaCedula.objects.filter(cedula=obj)
        return PracticaCedulaSerializer(relaciones, many=True).data
    
    def get_bibliografia(self, obj):
        relaciones = BibliografiaCedula.objects.filter(cedula=obj)
        return BibliografiaCedulaSerializer(relaciones, many=True).data
    
    def get_profesores_actuales(self, obj):
        relaciones = ProfesorActualCedula.objects.filter(cedula=obj)
        return ProfesorActualCedulaSerializer(relaciones, many=True).data
    
    def get_profesores_anteriores(self, obj):
        relaciones = ProfesorAnteriorCedula.objects.filter(cedula=obj)
        return ProfesorAnteriorCedulaSerializer(relaciones, many=True).data

class CursoInfoCedulaSerializer(serializers.ModelSerializer):
    curso = CursoSerializer(read_only=True)
    
    class Meta:
        model = CursoInfoCedula
        fields = ["id", "clave", "nombre", "seriacion", "ubicacion", "tipo", "objetivo_general", "numero_grupos"]

class CursoEjeCedulaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CursoEjeCedula
        fields = ["id", "nombre_eje", "horas"]

class CursoObjetivoEspecificoCedulaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CursoObjetivoEspecificoCedula
        fields = ["id", "descripcion"]

class HorasSemanaCedulaSerializer(serializers.ModelSerializer):
    class Meta:
        model = HorasSemanaCedula
        fields = ["id", "horas_totales", "horas_aula", "horas_laboratorio", "horas_practicas"]

class CursoEstadisticasCedulaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CursoEstadisticasCedula
        fields = ["id", "promedio", "porcentaje_mayores_iguales", "porcentaje_reprobados"]

class UnidadTematicaCedulaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnidadTematicaCedula
        fields = ["id", "descripcion"]

class EstrategiaEnsenanzaCedulaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstrategiaEnsenanzaCedula
        fields = ["id", "descripcion"]

class EstrategiaEvaluacionCedulaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstrategiaEvaluacionCedula
        fields = ["id", "descripcion"]

class PracticaCedulaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PracticaCedula
        fields = ["id", "descripcion"]

class BibliografiaCedulaSerializer(serializers.ModelSerializer):
    class Meta:
        model = BibliografiaCedula
        fields = ["id", "referencia"]

class ProfesorActualCedulaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfesorActualCedula
        fields = [
            "id", "nombres", "apellidos", "formacion_nombre", "experiencia_profesional",
        ]

class ProfesorAnteriorCedulaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfesorAnteriorCedula
        fields = [
            "id", "nombres", "apellidos", "formacion_nombre", "experiencia_profesional",
        ]
```
###tests.py
<p>
Esta clase sirve para importar los testsCase
</p>

```python
from django.test import TestCase.

# Create your tests here.
```
###urls.py
<p>
Esta clase sirve para crear las los links de las vistas.
</p>

```python
from rest_framework import routers

from cedulas.views import CedulaViewSet

router = routers.SimpleRouter()
router.register(r'', CedulaViewSet, basename='cedulas')
urlpatterns = router.urls
```

###views.py
<p>
Esta clase sirve para crear las vistas y mandar los datos del front-end a la base de datos.
</p>

```python
from rest_framework import viewsets

from cedulas.serializers import CedulaAEPVsAECACEISerializer, CedulaAEPVsOESerializer, CedulaCursosVsAEPSerializer, CedulaCvSinteticoSerializer, CedulaHerramientasValoracionAEPSerializer, CedulaOrganizacionCurricularSerializer, CedulaPlanMejoraSerializer, CedulaProgramaAsignaturaSerializer, CedulaValoracionObjetivosSerializer
from cedulas.models import Cedula

class CedulaViewSet(viewsets.ModelViewSet):
    queryset = Cedula.objects.all()
    
    def get_queryset(self):
        queryset = super().get_queryset()
        tipo = self.request.query_params.get("tipo")
        if tipo:
            queryset = queryset.filter(tipo=tipo)
        return queryset
    
    def get_serializer_class(self):
        # Si es retrieve/update
        if self.action in ["retrieve", "update", "partial_update"]:
            cedula = self.get_object()
            if cedula.tipo == Cedula.CV_SINTETICO:
                return CedulaCvSinteticoSerializer
            elif cedula.tipo == Cedula.PLAN_MEJORA:
                return CedulaPlanMejoraSerializer
            elif cedula.tipo == Cedula.VALORACION_OBJETIVOS:
                return CedulaValoracionObjetivosSerializer
            elif cedula.tipo == Cedula.AEP_VS_AECACEI:
                return CedulaAEPVsAECACEISerializer
            elif cedula.tipo == Cedula.AEP_VS_OE:
                return CedulaAEPVsOESerializer
            elif cedula.tipo == Cedula.CURSOS_VS_AEP:
                return CedulaCursosVsAEPSerializer
            elif cedula.tipo == Cedula.HERRAMIENTAS_VALORACION_AEP:
                return CedulaHerramientasValoracionAEPSerializer
            elif cedula.tipo == Cedula.PROGRAMA_ASIGNATURA:
                return CedulaProgramaAsignaturaSerializer
            return CedulaOrganizacionCurricularSerializer
        
        # Para create/list, usa el tipo desde request
        tipo = self.request.data.get("tipo") or self.request.query_params.get("tipo")
        if tipo == Cedula.CV_SINTETICO:
            return CedulaCvSinteticoSerializer
        elif tipo == Cedula.PLAN_MEJORA:
            return CedulaPlanMejoraSerializer
        elif tipo == Cedula.VALORACION_OBJETIVOS:
            return CedulaValoracionObjetivosSerializer
        elif tipo == Cedula.AEP_VS_AECACEI:
            return CedulaAEPVsAECACEISerializer
        elif tipo == Cedula.AEP_VS_OE:
            return CedulaAEPVsOESerializer
        elif tipo == Cedula.CURSOS_VS_AEP:
            return CedulaCursosVsAEPSerializer
        elif tipo == Cedula.HERRAMIENTAS_VALORACION_AEP:
            return CedulaHerramientasValoracionAEPSerializer
        elif tipo == Cedula.PROGRAMA_ASIGNATURA:
            return CedulaProgramaAsignaturaSerializer
        return CedulaOrganizacionCurricularSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        cedula_tipo = self.request.data.get("tipo") or self.request.query_params.get("tipo")
        # Incluir el curso en la serialización de EvaluacionIndicadorCedula
        context["include_curso"] = cedula_tipo == Cedula.HERRAMIENTAS_VALORACION_AEP
        return context
```

## Carpeta Core
###init.py
<p>
Esta clase sirve como un iniciador del la carpeta.
</p>

```python

```
###admin.py
<p>
Esta clase sirve para registrar las páginas de la carpeta.
</p>

```python
from django.contrib import admin
from core.models import Profesor, ProgramaEducativo, Curso, Institucion, Organizacion, Periodo

@admin.register(Profesor)
class ProfesorAdmin(admin.ModelAdmin):
    """Admin para el modelo Profesor"""
    list_display = ['numero_empleado', 'nombre_completo', 'nombramiento_actual', 'tiene_acceso_sistema', 'created_at']
    list_filter = ['experiencia_ingenieria', 'created_at']
    search_fields = ['numero_empleado', 'nombres', 'apellido_paterno', 'apellido_materno']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('numero_empleado', 'nombres', 'apellido_paterno', 'apellido_materno', 'fecha_nacimiento')
        }),
        ('Información Profesional', {
            'fields': ('nombramiento_actual', 'antiguedad', 'experiencia_ingenieria')
        }),
        ('Acceso al Sistema', {
            'fields': ('user',),
            'description': 'Vincular con un usuario para que el profesor tenga acceso como docente'
        }),
        ('Metadatos', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(ProgramaEducativo)
class ProgramaEducativoAdmin(admin.ModelAdmin):
    """Admin para ProgramaEducativo"""
    list_display = ['clave', 'nombre', 'estatus', 'fecha_creacion']
    list_filter = ['estatus', 'fecha_creacion']
    search_fields = ['clave', 'nombre']
    readonly_fields = ['fecha_creacion', 'created_at', 'updated_at']

@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    """Admin para Curso"""
    list_display = ['clave', 'nombre', 'programa', 'tipo', 'horas_totales']
    list_filter = ['tipo', 'programa']
    search_fields = ['clave', 'nombre']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Institucion)
class InstitucionAdmin(admin.ModelAdmin):
    """Admin para Institucion"""
    list_display = ['nombre', 'created_at']
    search_fields = ['nombre']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Organizacion)
class OrganizacionAdmin(admin.ModelAdmin):
    """Admin para Organizacion"""
    list_display = ['nombre', 'created_at']
    search_fields = ['nombre']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Periodo)
class PeriodoAdmin(admin.ModelAdmin):
    """Admin para Periodo"""
    list_display = ['nombre', 'semestre', 'anio', 'fecha_inicio', 'fecha_fin']
    list_filter = ['semestre', 'anio']
    search_fields = ['nombre']
    readonly_fields = ['nombre', 'created_at', 'updated_at']
```
###apps.py
<p>
Esta clase sirve para importar el django para las páginas.
</p>

```python
from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
```
###models.py
<p>
Esta clase sirve para importar los datos de la base de datos a las páginas.
</p>

```python
from django.db import models
from django.conf import settings

# Create your models here.
class Profesor(models.Model):
    """
    Modelo para representar a un Profesor.
    Si el profesor tiene un usuario tipo 'docente', puede acceder al sistema.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='profesor_profile',
        help_text='Usuario asociado si el profesor tiene acceso al sistema como docente'
    )
    numero_empleado = models.CharField(max_length=20, unique=True)
    apellido_paterno = models.CharField(max_length=50)
    apellido_materno = models.CharField(max_length=50)
    nombres = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    nombramiento_actual = models.CharField(max_length=100)
    antiguedad = models.PositiveSmallIntegerField()
    experiencia_ingenieria = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Profesor'
        verbose_name_plural = 'Profesores'
        ordering = ['apellido_paterno', 'apellido_materno', 'nombres']
        
    def __str__(self):
        return f"{self.nombres} {self.apellido_paterno} {self.apellido_materno}"
    
    @property
    def nombre_completo(self):
        return f"{self.nombres} {self.apellido_paterno} {self.apellido_materno}"
    
    @property
    def tiene_acceso_sistema(self):
        # Retorna si el profesor tiene un usuario asociado
        return self.user is not None

class ProgramaEducativo(models.Model):
    ACTIVO = 'activo'
    INACTIVO = 'inactivo'
    EN_REVISION = 'en_revision'

    ESTATUS_CHOICES = [
        (ACTIVO, 'Activo'),
        (INACTIVO, 'Inactivo'),
        (EN_REVISION, 'En Revisión'),
    ]

    clave = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateField(auto_now_add=True)
    estatus = models.CharField(max_length=20, choices=ESTATUS_CHOICES, default=ACTIVO)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

class Curso(models.Model):
    OBLIGATORIO = 'obligatorio'
    OPTATIVO = 'optativo'
    CURRICULAR = 'curricular'

    TIPO_CHOICES = [
        (OBLIGATORIO, 'Obligatorio'),
        (OPTATIVO, 'Optativo'),
        (CURRICULAR, 'Curricular'),
    ]
    
    programa = models.ForeignKey(ProgramaEducativo, on_delete=models.PROTECT)
    
    clave = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    seriacion = models.TextField(blank=True, null=True)
    ubicacion = models.CharField(max_length=50)
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES, default=OBLIGATORIO)
    horas_totales = models.IntegerField()
    objetivo_general = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.clave + " - " + self.nombre

class Institucion(models.Model):
    nombre = models.CharField(max_length=100)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

class Organizacion(models.Model):
    nombre = models.CharField(max_length=100)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

class Periodo(models.Model):
    SEMESTRE_CHOICES = [
        ('EM', 'Enero-Mayo'),
        ('AD', 'Agosto-Diciembre'),
    ]
    
    semestre = models.CharField(max_length=2, choices=SEMESTRE_CHOICES)
    anio = models.PositiveSmallIntegerField()
    nombre = models.CharField(max_length=6, editable=False)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        # Generar nombre automáticamente antes de guardar
        self.nombre = f"{self.semestre}{self.anio}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.nombre
```
###serializers.py
<p>
Esta clase sirve para consultar y actualizar la base de datos.
</p>

```python
from rest_framework import serializers

from core.models import Curso, Institucion, Organizacion, Periodo, Profesor, ProgramaEducativo

class ProfesorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profesor
        fields = ['id', 'numero_empleado', 'apellido_paterno', 'apellido_materno', 'nombres', 'fecha_nacimiento', 'nombramiento_actual', 'antiguedad', 'experiencia_ingenieria']
        read_only_fields = ['id']

class ProgramaEducativoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramaEducativo
        fields = ['id', 'clave', 'nombre', 'descripcion', 'fecha_creacion', 'estatus']
        read_only_fields = ['id']

class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = ['id', 'programa', 'clave', 'nombre', 'seriacion', 'ubicacion', 'tipo', 'horas_totales', 'objetivo_general']
        read_only_fields = ['id']

class InstitucionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institucion
        fields = ['id', 'nombre']
        read_only_fields = ['id']

class OrganizacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organizacion
        fields = ['id', 'nombre']
        read_only_fields = ['id']

class PeriodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Periodo
        fields = ['id',  'semestre', 'anio', 'nombre', 'fecha_inicio', 'fecha_fin']
        read_only_fields = ['id']
```
###serializers.py
<p>
Esta clase sirve para crear las vistas y mandar los datos del front-end a la base de datos
</p>

```python
from rest_framework import serializers

from core.models import Curso, Institucion, Organizacion, Periodo, Profesor, ProgramaEducativo

class ProfesorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profesor
        fields = ['id', 'numero_empleado', 'apellido_paterno', 'apellido_materno', 'nombres', 'fecha_nacimiento', 'nombramiento_actual', 'antiguedad', 'experiencia_ingenieria']
        read_only_fields = ['id']

class ProgramaEducativoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramaEducativo
        fields = ['id', 'clave', 'nombre', 'descripcion', 'fecha_creacion', 'estatus']
        read_only_fields = ['id']

class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = ['id', 'programa', 'clave', 'nombre', 'seriacion', 'ubicacion', 'tipo', 'horas_totales', 'objetivo_general']
        read_only_fields = ['id']

class InstitucionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institucion
        fields = ['id', 'nombre']
        read_only_fields = ['id']

class OrganizacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organizacion
        fields = ['id', 'nombre']
        read_only_fields = ['id']

class PeriodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Periodo
        fields = ['id',  'semestre', 'anio', 'nombre', 'fecha_inicio', 'fecha_fin']
        read_only_fields = ['id']
```
###tests.py
<p>
Esta clase sirve para importar los testsCase
</p>

```python
from django.test import TestCase

# Create your tests here.
```
###urls.py
<p>
Esta clase sirve para crear las los links de las vistas.
</p>

```python
from rest_framework import routers

from core.views import CursoViewSet, InstitucionViewSet, OrganizacionViewSet, PeriodoViewSet, ProfesorViewSet, ProgramaEducativoViewSet

router = routers.SimpleRouter()
router.register(r'profesores', ProfesorViewSet, basename='profesor')
router.register(r'programas_educativos', ProgramaEducativoViewSet, basename='programa-educativo')
router.register(r'cursos', CursoViewSet, basename='curso')
router.register(r'instituciones', InstitucionViewSet, basename='institucion')
router.register(r'organizaciones', OrganizacionViewSet, basename='organizacion')
router.register(r'periodos', PeriodoViewSet, basename='periodo')
urlpatterns = router.urls
```
###views.py
<p>
Esta clase sirve para crear las vistas y mandar los datos del front-end a la base de datos
</p>

```python
from rest_framework import viewsets

from core.models import Curso, Institucion, Organizacion, Periodo, Profesor, ProgramaEducativo
from core.serializers import CursoSerializer, InstitucionSerializer, OrganizacionSerializer, PeriodoSerializer, ProfesorSerializer, ProgramaEducativoSerializer

# Create your views here.
class ProfesorViewSet(viewsets.ModelViewSet):
    queryset = Profesor.objects.all()
    serializer_class = ProfesorSerializer

class ProgramaEducativoViewSet(viewsets.ModelViewSet):
    queryset = ProgramaEducativo.objects.all()
    serializer_class = ProgramaEducativoSerializer

class CursoViewSet(viewsets.ModelViewSet):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer

class InstitucionViewSet(viewsets.ModelViewSet):
    queryset = Institucion.objects.all()
    serializer_class = InstitucionSerializer

class OrganizacionViewSet(viewsets.ModelViewSet):
    queryset = Organizacion.objects.all()
    serializer_class = OrganizacionSerializer

class PeriodoViewSet(viewsets.ModelViewSet):
    queryset = Periodo.objects.all()
    serializer_class = PeriodoSerializer
```
## Carpeta Evaluacion_Acreditacion
###init.py
<p>
Esta clase sirve como un iniciador del la carpeta.
</p>

```python

```
###admin.py
<p>
Esta clase sirve para registrar las páginas de la carpeta.
</p>

```python
from django.contrib import admin

from evaluacion_acreditacion.models import AccionMejora, AportacionPE, Auditoria, EvaluacionIndicador, GestionAcademica, Hallazgo, Indicador

# Register your models here.
admin.site.register(AccionMejora)
admin.site.register(Indicador)
admin.site.register(EvaluacionIndicador)
admin.site.register(AportacionPE)
admin.site.register(GestionAcademica)
admin.site.register(Hallazgo)
admin.site.register(Auditoria)
```
###apps.py
<p>
Esta clase sirve para registrar las páginas de la carpeta.
</p>

```python
from django.apps import AppConfig


class EvaluacionAcreditacionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'evaluacion_acreditacion'
```
###models.py
<p>
Esta clase sirve para importar los datos de la base de datos a las páginas.
</p>

```python
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
```
###serializers.py
<p>
Esta clase sirve para consultar y actualizar la base de datos.
</p>

```python
from rest_framework import serializers

from evaluacion_acreditacion.models import AccionMejora, AportacionPE, EvaluacionIndicador, GestionAcademica, Hallazgo, Indicador, Auditoria

class AccionMejoraSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccionMejora
        fields = ['id', 'hallazgo', 'descripcion', 'resultado_esperado', 'meta', 'fecha_meta', 'responsable', 'estatus']
        read_only_fields = ['id']

class EvaluacionIndicadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvaluacionIndicador
        fields = ['id', 'indicador', 'curso', 'grupo_seccion', 'instrumento_evaluacion', 'descripcion_instrumento', 'periodo_evaluacion', 'valoracion', 'analisis_resultados', 'meta']
        read_only_fields = ['id']

class IndicadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Indicador
        fields = ['id', 'criterio', 'codigo', 'descripcion']
        read_only_fields = ['id']

class AportacionPESerializer(serializers.ModelSerializer):
    class Meta:
        model = AportacionPE
        fields = ['id', 'profesor', 'descripcion']
        read_only_fields = ['id']

class GestionAcademicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = GestionAcademica
        fields = ['id', 'profesor', 'institucion', 'actividad', 'fecha_inicio', 'fecha_fin']
        read_only_fields = ['id']

class HallazgoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hallazgo
        fields = ['id', 'programa', 'numero_hallazgo', 'descripcion', 'objetivo', 'atributo_pe', 'es_indice_rendimiento', 'indicador_mr2025']
        read_only_fields = ['id']

class AuditoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auditoria
        fields = ['id', 'accion', 'tabla_afectada', 'registro_id', 'datos_anteriores', 'datos_nuevos', 'ip_address', 'user_agent']
        read_only_fields = ['id']
```
###tests.py
<p>
Esta clase sirve para importar los testsCase.
</p>

```python
from django.test import TestCase

# Create your tests here.
```
###urls.py
<p>
Esta clase sirve para crear las los links de las vistas.
</p>

```python
from rest_framework import routers

from evaluacion_acreditacion.views import (
    AccionMejoraViewSet,
    IndicadorViewSet,
    EvaluacionIndicadorViewSet,
    AportacionPEViewSet,
    GestionAcademicaViewSet,
    HallazgoViewSet,
    AuditoriaViewSet
)

router = routers.SimpleRouter()
router.register(r'acciones_mejora', AccionMejoraViewSet, basename='accion-mejora')
router.register(r'indicadores', IndicadorViewSet, basename='indicador')
router.register(r'evaluaciones_indicador', EvaluacionIndicadorViewSet, basename='evaluacion-indicador') 
router.register(r'aportaciones_pe', AportacionPEViewSet, basename='aportacion-pe')
router.register(r'gestion_academica', GestionAcademicaViewSet, basename='gestion-academica')
router.register(r'hallazgos', HallazgoViewSet, basename='hallazgo')
router.register(r'auditorias', AuditoriaViewSet, basename='auditoria')
urlpatterns = router.urls
```
###views.py
<p>
Esta clase sirve para crear las vistas y mandar los datos del front-end a la base de datos.
</p>

```python
from rest_framework import viewsets

from evaluacion_acreditacion.models import AccionMejora, Indicador, EvaluacionIndicador, AportacionPE, GestionAcademica, Hallazgo, Auditoria
from evaluacion_acreditacion.serializers import AccionMejoraSerializer, IndicadorSerializer, EvaluacionIndicadorSerializer, AportacionPESerializer, GestionAcademicaSerializer, HallazgoSerializer, AuditoriaSerializer

# Create your views here.
class AccionMejoraViewSet(viewsets.ModelViewSet):
    queryset = AccionMejora.objects.all()
    serializer_class = AccionMejoraSerializer

class IndicadorViewSet(viewsets.ModelViewSet):
    queryset = Indicador.objects.all()
    serializer_class = IndicadorSerializer

class EvaluacionIndicadorViewSet(viewsets.ModelViewSet):
    queryset = EvaluacionIndicador.objects.all()
    serializer_class = EvaluacionIndicadorSerializer

class AportacionPEViewSet(viewsets.ModelViewSet):
    queryset = AportacionPE.objects.all()
    serializer_class = AportacionPESerializer

class GestionAcademicaViewSet(viewsets.ModelViewSet):
    queryset = GestionAcademica.objects.all()
    serializer_class = GestionAcademicaSerializer

class HallazgoViewSet(viewsets.ModelViewSet):
    queryset = Hallazgo.objects.all()
    serializer_class = HallazgoSerializer

class AuditoriaViewSet(viewsets.ModelViewSet):
    queryset = Auditoria.objects.all()
    serializer_class = AuditoriaSerializer::
```
## Carpeta Gestion Academica
###init.py
<p>
Esta clase sirve como un iniciador del la carpeta.
</p>

```python

```
###admin.py
<p>
Esta clase sirve para registrar las páginas de la carpeta.
</p>

```python
from django.contrib import admin

from gestion_academica.models import Alumno, AtributoCACEI, AtributoPE, AtributoPECACEI, AtributoPEObjetivo, Bibliografia, Calificacion, CriterioDesempeno, CursoAtributoPE, CursoEje, EjeConocimiento, EstrategiaEnsenanza, EstrategiaEvaluacion, HorasSemana, ObjetivoEducacional, ObjetivoEspecifico, Practica, UnidadTematica

# Register your models here.
admin.site.register(UnidadTematica)
admin.site.register(CriterioDesempeno)
admin.site.register(EstrategiaEnsenanza)
admin.site.register(EstrategiaEvaluacion)
admin.site.register(ObjetivoEducacional)
admin.site.register(Bibliografia)
admin.site.register(HorasSemana)
admin.site.register(EjeConocimiento)
admin.site.register(ObjetivoEspecifico)
admin.site.register(AtributoPE)
admin.site.register(AtributoCACEI)
admin.site.register(CursoAtributoPE)
admin.site.register(CursoEje)
admin.site.register(AtributoPEObjetivo)
admin.site.register(AtributoPECACEI)
admin.site.register(Practica)
admin.site.register(Alumno)
admin.site.register(Calificacion)
```
###apps.py
<p>
Esta clase sirve para registrar las páginas de la carpeta.
</p>

```python
from django.apps import AppConfig


class GestionAcademicaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gestion_academica'
```
###models.py
<p>
Esta clase sirve para importar los datos de la base de datos a las páginas.
</p>

```python
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
        return f"{self.autor}. ({self.anio_publicacion}). {self.titulo}. {self.editorial}."

class HorasSemana(models.Model):
    curso = models.ForeignKey('core.Curso', on_delete=models.PROTECT)
    
    horas_totales = models.PositiveSmallIntegerField()
    horas_aula = models.PositiveSmallIntegerField()
    horas_laboratorio = models.PositiveSmallIntegerField()
    horas_practicas = models.PositiveSmallIntegerField()
    
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
```
###serializers.py
<p>
Esta clase sirve para consultar y actualizar la base de datos.
</p>

```python
from rest_framework import serializers

from gestion_academica.models import Alumno, AtributoCACEI, AtributoPE, AtributoPECACEI, AtributoPEObjetivo, Bibliografia, Calificacion, CriterioDesempeno, CursoAtributoPE, CursoEje, EjeConocimiento, EstrategiaEnsenanza, EstrategiaEvaluacion, HorasSemana, ObjetivoEducacional, ObjetivoEspecifico, Practica, UnidadTematica

class UnidadTematicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnidadTematica
        fields = ['id', 'curso', 'numero', 'descripcion']
        read_only_fields = ['id']

class CriterioDesempenoSerializer(serializers.ModelSerializer):    
    class Meta:
        model = CriterioDesempeno
        fields = ['id', 'atributo_pe', 'codigo', 'descripcion']
        read_only_fields = ['id']

class EstrategiaEnsenanzaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstrategiaEnsenanza
        fields = ['id', 'curso', 'numero', 'descripcion']
        read_only_fields = ['id']

class EstrategiaEvaluacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstrategiaEvaluacion
        fields = ['id', 'curso', 'numero', 'descripcion']
        read_only_fields = ['id']

class ObjetivoEducacionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObjetivoEducacional
        fields = ['id', 'programa', 'codigo', 'descripcion']
        read_only_fields = ['id']

class BibliografiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bibliografia
        fields = ['id', 'curso', 'numero', 'autor', 'titulo', 'editorial', 'anio_publicacion']
        read_only_fields = ['id']

class HorasSemanaSerializer(serializers.ModelSerializer):
    class Meta:
        model = HorasSemana
        fields = ['id', 'curso', 'horas_totales', 'horas_aula', 'horas_laboratorio', 'horas_practicas', 'numero_grupos', 'calificacion_promedio', 'porcentaje_aprobacion', 'porcentaje_reprobacion']
        read_only_fields = ['id']

class EjeConocimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EjeConocimiento
        fields = ['id', 'nombre', 'descripcion']
        read_only_fields = ['id']

class ObjetivoEspecificoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObjetivoEspecifico
        fields = ['id', 'curso', 'descripcion', 'orden']
        read_only_fields = ['id']

class AtributoCACEISerializer(serializers.ModelSerializer):
    class Meta:
        model = AtributoCACEI
        fields = ['id', 'codigo', 'nombre', 'descripcion', 'wk_referencia']
        read_only_fields = ['id']

class AtributoPECACEISerializer(serializers.ModelSerializer):
    class Meta:
        model = AtributoPECACEI
        fields = ['id', 'atributo_pe', 'atributo_cacei', 'justificacion']
        read_only_fields = ['id']

class AtributoPEObjetivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AtributoPEObjetivo
        fields = ['id', 'atributo_pe', 'objetivo', 'justificacion']
        read_only_fields = ['id']

class AtributoPESerializer(serializers.ModelSerializer):
    class Meta:
        model = AtributoPE
        fields = ['id', 'programa', 'codigo', 'nombre', 'nombre_abreviado', 'descripcion']
        read_only_fields = ['id']

class CursoAtributoPESerializer(serializers.ModelSerializer):
    class Meta:
        model = CursoAtributoPE
        fields = ['id', 'curso', 'atributo_pe', 'nivel_aporte']
        read_only_fields = ['id']

class CursoEjeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CursoEje
        fields = ['id', 'curso', 'eje', 'horas']
        read_only_fields = ['id']

class PracticaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Practica
        fields = ['id', 'curso', 'numero', 'descripcion']
        read_only_fields = ['id']

class AlumnoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alumno
        fields = ['id', 'matricula', 'nombre', 'apellido1', 'apellido2']
        read_only_fields = ['id']

class CalificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calificacion
        fields = ['id', 'alumno', 'profesor_curso', 'valor']
        read_only_fields = ['id']
```
###tests.py
<p>
Esta clase sirve para importar los testsCase.
</p>

```python
from django.test import TestCase

# Create your tests here.
```
###urls.py
<p>
Esta clase sirve para crear las los links de las vistas.
</p>

```python
from rest_framework import routers

from gestion_academica.views import AlumnoViewSet, AtributoCACEIViewSet, AtributoPECACEIViewSet, AtributoPEObjetivoViewSet, AtributoPEViewSet, BibliografiaViewSet, CalificacionViewSet, CriterioDesempenoViewSet, CursoAtributoPEViewSet, CursoEjeViewSet, EjeConocimientoViewSet, EstrategiaEnsenanzaViewSet, EstrategiaEvaluacionViewSet, HorasSemanaViewSet, ObjetivoEducacionalViewSet, ObjetivoEspecificoViewSet, PracticaViewSet, UnidadTematicaViewSet

router = routers.SimpleRouter()
router.register(r'unidades_tematicas', UnidadTematicaViewSet, basename='unidad-tematica')
router.register(r'criterios_desempeno', CriterioDesempenoViewSet, basename='criterio-desempeno')
router.register(r'estrategias_ensenanza', EstrategiaEnsenanzaViewSet, basename='estrategia-ensenanza')
router.register(r'estrategias_evaluacion', EstrategiaEvaluacionViewSet, basename='estrategia-evaluacion')
router.register(r'objetivos_educacionales', ObjetivoEducacionalViewSet, basename='objetivo-educacional')
router.register(r'bibliografia', BibliografiaViewSet, basename='bibliografia')
router.register(r'horas_semana', HorasSemanaViewSet, basename='horas-semana')
router.register(r'ejes_conocimiento', EjeConocimientoViewSet, basename='eje-conocimiento')
router.register(r'objetivos_especificos', ObjetivoEspecificoViewSet, basename='objetivo-especifico')
router.register(r'atributos_pe', AtributoPEViewSet, basename='atributo-pe')
router.register(r'atributos_cacei', AtributoCACEIViewSet, basename='atributo-cacei')
router.register(r'cursos_atributos_pe', CursoAtributoPEViewSet, basename='curso-atributo-pe')
router.register(r'cursos_ejes', CursoEjeViewSet, basename='curso-eje')
router.register(r'atributos_pe_objetivos', AtributoPEObjetivoViewSet, basename='atributo-pe-objetivo')
router.register(r'atributos_pe_cacei', AtributoPECACEIViewSet, basename='atributo-pe-cacei')
router.register(r'practicas', PracticaViewSet, basename='practica')
router.register(r'alumnos', AlumnoViewSet, basename='alumno')
router.register(r'calificaciones', CalificacionViewSet, basename='calificacion')
urlpatterns = router.urls
```
###views.py
<p>
Esta clase sirve para crear las vistas y mandar los datos del front-end a la base de datos.
</p>

```python
from rest_framework import viewsets

from gestion_academica.models import Alumno, AtributoCACEI, AtributoPE, AtributoPECACEI, AtributoPEObjetivo, Bibliografia, Calificacion, CriterioDesempeno, CursoAtributoPE, CursoEje, EjeConocimiento, EstrategiaEnsenanza, EstrategiaEvaluacion, HorasSemana, ObjetivoEducacional, ObjetivoEspecifico, Practica, UnidadTematica
from gestion_academica.serializers import AlumnoSerializer, AtributoCACEISerializer, AtributoPECACEISerializer, AtributoPEObjetivoSerializer, AtributoPESerializer, BibliografiaSerializer, CalificacionSerializer, CriterioDesempenoSerializer, CursoAtributoPESerializer, CursoEjeSerializer, EjeConocimientoSerializer, EstrategiaEnsenanzaSerializer, EstrategiaEvaluacionSerializer, HorasSemanaSerializer, ObjetivoEducacionalSerializer, ObjetivoEspecificoSerializer, PracticaSerializer, UnidadTematicaSerializer

# Create your views here.
class UnidadTematicaViewSet(viewsets.ModelViewSet):
    queryset = UnidadTematica.objects.all()
    serializer_class = UnidadTematicaSerializer
    
class CriterioDesempenoViewSet(viewsets.ModelViewSet):
    queryset = CriterioDesempeno.objects.all()
    serializer_class = CriterioDesempenoSerializer

class EstrategiaEnsenanzaViewSet(viewsets.ModelViewSet):
    queryset = EstrategiaEnsenanza.objects.all()
    serializer_class = EstrategiaEnsenanzaSerializer

class EstrategiaEvaluacionViewSet(viewsets.ModelViewSet):
    queryset = EstrategiaEvaluacion.objects.all()
    serializer_class = EstrategiaEvaluacionSerializer

class ObjetivoEducacionalViewSet(viewsets.ModelViewSet):
    queryset = ObjetivoEducacional.objects.all()
    serializer_class = ObjetivoEducacionalSerializer

class BibliografiaViewSet(viewsets.ModelViewSet):
    queryset = Bibliografia.objects.all()
    serializer_class = BibliografiaSerializer

class HorasSemanaViewSet(viewsets.ModelViewSet):
    queryset = HorasSemana.objects.all()
    serializer_class = HorasSemanaSerializer

class EjeConocimientoViewSet(viewsets.ModelViewSet):
    queryset = EjeConocimiento.objects.all()
    serializer_class = EjeConocimientoSerializer

class ObjetivoEspecificoViewSet(viewsets.ModelViewSet):
    queryset = ObjetivoEspecifico.objects.all()
    serializer_class = ObjetivoEspecificoSerializer

class AtributoPEViewSet(viewsets.ModelViewSet):
    queryset = AtributoPE.objects.all()
    serializer_class = AtributoPESerializer

class AtributoCACEIViewSet(viewsets.ModelViewSet):
    queryset = AtributoCACEI.objects.all()
    serializer_class = AtributoCACEISerializer

class CursoAtributoPEViewSet(viewsets.ModelViewSet):
    queryset = CursoAtributoPE.objects.all()
    serializer_class = CursoAtributoPESerializer

class CursoEjeViewSet(viewsets.ModelViewSet):
    queryset = CursoEje.objects.all()
    serializer_class = CursoEjeSerializer

class AtributoPEObjetivoViewSet(viewsets.ModelViewSet):
    queryset = AtributoPEObjetivo.objects.all()
    serializer_class = AtributoPEObjetivoSerializer

class AtributoPECACEIViewSet(viewsets.ModelViewSet):
    queryset = AtributoPECACEI.objects.all()
    serializer_class = AtributoPECACEISerializer

class PracticaViewSet(viewsets.ModelViewSet):
    queryset = Practica.objects.all()
    serializer_class = PracticaSerializer

class AlumnoViewSet(viewsets.ModelViewSet):
    queryset = Alumno.objects.all()
    serializer_class = AlumnoSerializer

class CalificacionViewSet(viewsets.ModelViewSet):
    queryset = Calificacion.objects.all()
    serializer_class = CalificacionSerializer::
```
## Carpeta Gestion de Profesores
###init.py
<p>
Esta clase sirve como un iniciador del la carpeta.
</p>

```python

```
###admin.py
<p>
Esta clase sirve para registrar las páginas de la carpeta.
</p>

```python
from django.contrib import admin

from gestion_de_profesores.models import ActualizacionDisciplinar, CapacitacionDocente, ExperienciaDiseno, ExperienciaProfesional, FormacionAcademica, LogroProfesional, ParticipacionOrganizaciones, PremioDistincion, ProductoAcademico, ProfesorCurso

# Register your models here.
admin.site.register(ProfesorCurso)
admin.site.register(FormacionAcademica)
admin.site.register(ExperienciaProfesional)
admin.site.register(ExperienciaDiseno)
admin.site.register(LogroProfesional)
admin.site.register(PremioDistincion)
admin.site.register(ParticipacionOrganizaciones)
admin.site.register(CapacitacionDocente)
admin.site.register(ActualizacionDisciplinar)
admin.site.register(ProductoAcademico)

```
###apps.py
<p>
Esta clase sirve para registrar las páginas de la carpeta.
</p>

```python
from django.apps import AppConfig


class GestionDeProfesoresConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gestion_de_profesores'

```
###models.py
<p>
Esta clase sirve para importar los datos de la base de datos a las páginas.
</p>

```python
from django.db import models

# Create your models here.
class ProfesorCurso(models.Model):
    RESPONSABLE = 'responsable'
    INSTRUCTOR = 'instructor'

    TIPO_CHOICES = [
        (RESPONSABLE, 'Responsable'),
        (INSTRUCTOR, 'Instructor'),
    ]

    profesor = models.ForeignKey('core.Profesor', on_delete=models.PROTECT)
    curso = models.ForeignKey('core.Curso', on_delete=models.PROTECT)
    periodo = models.ForeignKey('core.Periodo', on_delete=models.PROTECT)
    
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default=RESPONSABLE)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.curso.clave} {self.curso.nombre} - {str(self.profesor)} ({self.periodo.nombre})"

class FormacionAcademica(models.Model):
    LICENCIATURA = 'licenciatura'
    ESPECIALIDAD = 'especialidad'
    MAESTRIA = 'maestria'
    DOCTORADO = 'doctorado'

    NIVEL_CHOICES = [
        (LICENCIATURA, 'Licenciatura'),
        (ESPECIALIDAD, 'Especialidad'),
        (MAESTRIA, 'Maestría'),
        (DOCTORADO, 'Doctorado'),
    ]

    profesor = models.ForeignKey('core.Profesor', on_delete=models.PROTECT)
    institucion = models.ForeignKey('core.Institucion', on_delete=models.PROTECT)
    
    nivel = models.CharField(max_length=20, choices=NIVEL_CHOICES, default=LICENCIATURA)
    nombre = models.CharField(max_length=100)
    pais = models.CharField(max_length=50)
    anio_obtencion = models.PositiveSmallIntegerField()
    cedula_profesional = models.CharField(max_length=50, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{str(self.profesor)} tiene formacion academica de {self.nivel}"

class ExperienciaProfesional(models.Model):
    profesor = models.ForeignKey('core.Profesor', on_delete=models.PROTECT)
    organizacion = models.ForeignKey('core.Organizacion', on_delete=models.PROTECT)
    
    puesto = models.CharField(max_length=100)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    actividades = models.TextField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{str(self.profesor)} trabajó en {self.organizacion.nombre} como {self.puesto}"
    
class ExperienciaDiseno(models.Model):
    profesor = models.ForeignKey('core.Profesor', on_delete=models.PROTECT)
    organizacion = models.ForeignKey('core.Organizacion', on_delete=models.PROTECT)
    
    periodo = models.CharField(max_length=50)
    nivel_experiencia = models.CharField(max_length=50)
    descripcion = models.TextField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{str(self.profesor)} tiene experiencia de diseño de {self.nivel_experiencia} en {self.organizacion.nombre}"

class LogroProfesional(models.Model):
    profesor = models.ForeignKey('core.Profesor', on_delete=models.PROTECT)
    
    descripcion = models.TextField()
    anio = models.PositiveSmallIntegerField(null=True, blank=True)
    relevancia = models.TextField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{str(self.profesor)} tiene logros de {self.descripcion} en {self.anio}"

class PremioDistincion(models.Model):
    profesor = models.ForeignKey('core.Profesor', on_delete=models.PROTECT)
    institucion_otorga = models.ForeignKey('core.Organizacion', on_delete=models.PROTECT)
    
    descripcion = models.TextField()
    anio = models.PositiveSmallIntegerField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{str(self.profesor)} recibió el premio {self.descripcion} en {self.anio}"

class ParticipacionOrganizaciones(models.Model):
    profesor = models.ForeignKey('core.Profesor', on_delete=models.PROTECT)
    organizacion = models.ForeignKey('core.Organizacion', on_delete=models.PROTECT)
    
    periodo = models.CharField(max_length=50)
    nivel_participacion = models.CharField(max_length=50)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{str(self.profesor)} participó en {self.organizacion.nombre}"

class CapacitacionDocente(models.Model):
    profesor = models.ForeignKey('core.Profesor', on_delete=models.PROTECT)
    institucion = models.ForeignKey('core.Institucion', on_delete=models.PROTECT)
    
    nombre_curso = models.CharField(max_length=100)
    pais = models.CharField(max_length=50)
    anio_obtencion = models.PositiveSmallIntegerField()
    horas = models.PositiveSmallIntegerField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{str(self.profesor)} recibió esta capacitación docente {self.nombre_curso}"

class ActualizacionDisciplinar(models.Model):
    profesor = models.ForeignKey('core.Profesor', on_delete=models.PROTECT)
    institucion = models.ForeignKey('core.Institucion', on_delete=models.PROTECT)
    
    nombre_curso = models.CharField(max_length=100)
    pais = models.CharField(max_length=50)
    anio_obtencion = models.PositiveSmallIntegerField()
    horas = models.PositiveSmallIntegerField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{str(self.profesor)} recibió esta actualización disciplinar {self.nombre_curso}"

class ProductoAcademico(models.Model):
    PUBLICACION = 'publicacion'
    PROYECTO = 'proyecto'
    PATENTE = 'patente'
    OTRO = 'otro'

    TIPO_CHOICES = [
        (PUBLICACION, 'Publicación'),
        (PROYECTO, 'Proyecto'),
        (PATENTE, 'Patente'),
        (OTRO, 'Otro'),
    ]
    
    profesor = models.ForeignKey('core.Profesor', on_delete=models.PROTECT)

    descripcion = models.TextField()
    anio = models.PositiveSmallIntegerField()
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default=PUBLICACION)
    detalles = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Producto académico: {self.descripcion} ({self.tipo})"
```
###serializers.py
<p>
Esta clase sirve para consultar y actualizar la base de datos.
</p>

```python
from rest_framework import serializers

from gestion_de_profesores.models import ActualizacionDisciplinar, CapacitacionDocente, ExperienciaDiseno, ExperienciaProfesional, FormacionAcademica, LogroProfesional, ParticipacionOrganizaciones, PremioDistincion, ProductoAcademico, ProfesorCurso

class ProfesorCursoSerializer(serializers.ModelSerializer):    
    class Meta:
        model = ProfesorCurso
        fields = ['id', 'profesor', 'curso', 'tipo', 'periodo']
        read_only_fields = ['id']

class FormacionAcademicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormacionAcademica
        fields = ['id', 'profesor', 'institucion', 'nivel', 'pais', 'anio_obtencion', 'cedula_profesional', 'especialidad']
        read_only_fields = ['id']

class ExperienciaProfesionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExperienciaProfesional
        fields = ['id', 'profesor', 'organizacion', 'puesto', 'fecha_inicio', 'fecha_fin', 'actividades']
        read_only_fields = ['id']

class ExperienciaDisenoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExperienciaDiseno
        fields = ['id', 'profesor', 'organizacion', 'periodo', 'nivel_experiencia', 'descripcion']
        read_only_fields = ['id']

class LogroProfesionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogroProfesional
        fields = ['id', 'profesor', 'descripcion', 'anio', 'relevancia']
        read_only_fields = ['id']

class PremioDistincionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PremioDistincion
        fields = ['id', 'profesor', 'descripcion', 'anio', 'institucion_otorga']
        read_only_fields = ['id']

class ParticipacionOrganizacionesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParticipacionOrganizaciones
        fields = ['id', 'profesor', 'organizacion', 'periodo', 'nivel_participacion']
        read_only_fields = ['id']

class CapacitacionDocenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CapacitacionDocente
        fields = ['id', 'profesor', 'institucion', 'nombre_curso', 'pais', 'anio_obtencion', 'horas']
        read_only_fields = ['id']

class ActualizacionDisciplinarSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActualizacionDisciplinar
        fields = ['id', 'profesor', 'institucion', 'nombre_curso', 'pais', 'anio_obtencion', 'horas']
        read_only_fields = ['id']

class ProductoAcademicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductoAcademico
        fields = ['id', 'profesor', 'descripcion', 'anio', 'tipo', 'detalles']
        read_only_fields = ['id']
```
###tests.py
<p>
Esta clase sirve para importar los testsCase.
</p>

```python
from django.test import TestCase

# Create your tests here.
```
###urls.py
<p>
Esta clase sirve para crear las los links de las vistas.
</p>

```python

from rest_framework import routers

from gestion_de_profesores.views import ActualizacionDisciplinarViewSet, CapacitacionDocenteViewSet, ExperienciaDisenoViewSet, ExperienciaProfesionalViewSet, FormacionAcademicaViewSet, LogroProfesionalViewSet, ParticipacionOrganizacionesViewSet, PremioDistincionViewSet, ProductoAcademicoViewSet, ProfesorCursoViewSet

router = routers.SimpleRouter()
router.register(r'profesores_cursos', ProfesorCursoViewSet, basename='profesor-curso')
router.register(r'formacion_academica', FormacionAcademicaViewSet, basename='formacion-academica')
router.register(r'experiencia_profesional', ExperienciaProfesionalViewSet, basename='experiencia-profesional')
router.register(r'experiencia_diseno', ExperienciaDisenoViewSet, basename='experiencia-diseno')
router.register(r'logros_profesionales', LogroProfesionalViewSet, basename='logro-profesional')
router.register(r'premios_distincion', PremioDistincionViewSet, basename='premio-distincion')
router.register(r'participacion_organizaciones', ParticipacionOrganizacionesViewSet, basename='participacion-organizaciones')
router.register(r'capacitacion_docente', CapacitacionDocenteViewSet, basename='capacitacion-docente')
router.register(r'actualizacion_disciplinar', ActualizacionDisciplinarViewSet, basename='actualizacion-disciplinar')
router.register(r'productos_academicos', ProductoAcademicoViewSet, basename='producto-academico')
urlpatterns = router.urls

```
###views.py
<p>
Esta clase sirve para crear las vistas y mandar los datos del front-end a la base de datos.
</p>

```python
from rest_framework import viewsets

from gestion_de_profesores.models import ActualizacionDisciplinar, CapacitacionDocente, ExperienciaDiseno, ExperienciaProfesional, FormacionAcademica, LogroProfesional, ParticipacionOrganizaciones, PremioDistincion, ProductoAcademico, ProfesorCurso
from gestion_de_profesores.serializers import ActualizacionDisciplinarSerializer, CapacitacionDocenteSerializer, ExperienciaDisenoSerializer, ExperienciaProfesionalSerializer, FormacionAcademicaSerializer, LogroProfesionalSerializer, ParticipacionOrganizacionesSerializer, PremioDistincionSerializer, ProductoAcademicoSerializer, ProfesorCursoSerializer

# Create your views here.
class ProfesorCursoViewSet(viewsets.ModelViewSet):
    queryset = ProfesorCurso.objects.all()
    serializer_class = ProfesorCursoSerializer

class FormacionAcademicaViewSet(viewsets.ModelViewSet):
    queryset = FormacionAcademica.objects.all()
    serializer_class = FormacionAcademicaSerializer

class ExperienciaProfesionalViewSet(viewsets.ModelViewSet):
    queryset = ExperienciaProfesional.objects.all()
    serializer_class = ExperienciaProfesionalSerializer

class ExperienciaDisenoViewSet(viewsets.ModelViewSet):
    queryset = ExperienciaDiseno.objects.all()
    serializer_class = ExperienciaDisenoSerializer

class LogroProfesionalViewSet(viewsets.ModelViewSet):
    queryset = LogroProfesional.objects.all()
    serializer_class = LogroProfesionalSerializer

class PremioDistincionViewSet(viewsets.ModelViewSet):
    queryset = PremioDistincion.objects.all()
    serializer_class = PremioDistincionSerializer

class ParticipacionOrganizacionesViewSet(viewsets.ModelViewSet):
    queryset = ParticipacionOrganizaciones.objects.all()
    serializer_class = ParticipacionOrganizacionesSerializer

class CapacitacionDocenteViewSet(viewsets.ModelViewSet):
    queryset = CapacitacionDocente.objects.all()
    serializer_class = CapacitacionDocenteSerializer

class ActualizacionDisciplinarViewSet(viewsets.ModelViewSet):
    queryset = ActualizacionDisciplinar.objects.all()
    serializer_class = ActualizacionDisciplinarSerializer

class ProductoAcademicoViewSet(viewsets.ModelViewSet):
    queryset = ProductoAcademico.objects.all()
    serializer_class = ProductoAcademicoSerializer::
```
## Carpeta Usuarios y Acceso
###init.py
<p>
Esta clase sirve como un iniciador del la carpeta.
</p>

```python

```
###admin.py
<p>
Esta clase sirve para registrar las páginas de la carpeta.
</p>

```python
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from usuarios_y_acceso.models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # Admin personalizado para CustomUser
    list_display = ['username', 'email', 'role', 'first_name', 'last_name', 'is_active', 'date_joined']
    list_filter = ['role', 'is_active', 'is_staff', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['-date_joined']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Información Adicional', {'fields': ('role',)}),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información Adicional', {'fields': ('role', 'email', 'first_name', 'last_name')}),
    )
```
###apps.py
<p>
Esta clase sirve para registrar las páginas de la carpeta.
</p>

```python
from django.apps import AppConfig


class UsuariosYAccesoonfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'usuarios_y_acceso'

```
###models.py
<p>
Esta clase sirve para importar los datos de la base de datos a las páginas.
</p>

```python
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
class CustomUser(AbstractUser):
    """
    Usuario personalizado con tres roles:
    - Admin: Acceso completo a todo el sistema
    - Coordinador: Puede gestionar profesores, cursos, evaluaciones
    - Docente: Solo puede ver/editar su propia información como profesor
    """
    ADMIN = 'admin'
    COORDINADOR = 'coordinador'
    DOCENTE = 'docente'
    
    ROLE_CHOICES = [
        (ADMIN, 'Administrador'),
        (COORDINADOR, 'Coordinador'),
        (DOCENTE, 'Docente'),
    ]
    
    role = models.CharField(
        max_length=20, 
        choices=ROLE_CHOICES, 
        default=DOCENTE,
        help_text='Rol del usuario en el sistema'
    )
    
    # Overridear groups y user_permissions para evitar conflictos con AbstractUser
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name="customuser_set",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="customuser_set",
        related_query_name="user",
    )

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['username']

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    @property
    def is_admin(self):
        return self.role == self.ADMIN
    
    @property
    def is_coordinador(self):
        return self.role == self.COORDINADOR
    
    @property
    def is_docente(self):
        return self.role == self.DOCENTE
    
    @property
    def tiene_profesor_asociado(self):
        return hasattr(self, 'profesor_profile')
    
    def clean(self):
        super().clean()
        # Si es docente, debe tener email
        if self.role == self.DOCENTE and not self.email:
            raise ValidationError('Los docentes deben tener un email registrado.')
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
```
###permissions.py
<p>
Esta clase sirve para revisar los permisos de los usuarios.
</p>

```python
from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    # Permiso para usuarios con rol de administrador
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin

class IsCoordinadorOrAdmin(permissions.BasePermission):
    """
    Permiso para coordinadores y administradores   
    Útil para endpoints de gestión general
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['admin', 'coordinador']

class IsDocenteOwner(permissions.BasePermission):
    """
    Permiso para que docentes solo accedan a sus propios datos
    Admin y Coordinador pueden acceder a todo
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Admin y Coordinador tienen acceso total
        if request.user.role in ['admin', 'coordinador']:
            return True
        
        # Docente solo puede acceder a sus propios datos
        if request.user.is_docente:
            # Verificar si el objeto tiene relación con el profesor del usuario
            if hasattr(obj, 'profesor'):
                return obj.profesor.user == request.user
            # Si el objeto ES el profesor
            if hasattr(obj, 'user'):
                return obj.user == request.user
        
        return False

class ReadOnly(permissions.BasePermission):
    # Permiso de solo lectura para cualquier usuario autenticado
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.method in permissions.SAFE_METHODS

class IsDocenteOrReadOnly(permissions.BasePermission):
    """
    Los docentes pueden leer todo pero solo modificar sus datos
    Admin y Coordinador pueden todo
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Lectura permitida para todos
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Admin y Coordinador pueden modificar todo
        if request.user.role in ['admin', 'coordinador']:
            return True
        
        # Docente solo puede modificar sus propios datos
        if request.user.is_docente:
            if hasattr(obj, 'profesor'):
                return obj.profesor.user == request.user
            if hasattr(obj, 'user'):
                return obj.user == request.user
        
        return False
```
###serializers.py
<p>
Esta clase sirve para consultar y actualizar la base de datos.
</p>

```python
from rest_framework import serializers

from usuarios_y_acceso.models import CustomUser
from core.models import Profesor

class UserSerializer(serializers.ModelSerializer):
    # Serializer para mostrar información del usuario
    profesor_id = serializers.SerializerMethodField()
    profesor_nombre = serializers.SerializerMethodField()
    
    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'role', 
            'is_active', 'profesor_id', 'profesor_nombre', 'date_joined'
        ]
        read_only_fields = ['id', 'date_joined', 'profesor_id', 'profesor_nombre']
    
    def get_profesor_id(self, obj):
        # Retorna el ID del profesor si existe
        if obj.is_docente and obj.tiene_profesor_asociado:
            return obj.profesor_profile.id
        return None
    
    def get_profesor_nombre(self, obj):
        # Retorna el nombre completo del profesor si existe
        if obj.is_docente and obj.tiene_profesor_asociado:
            return obj.profesor_profile.nombre_completo
        return None

class UserRegisterSerializer(serializers.ModelSerializer):
    # Serializer para registro de nuevos usuarios
    password = serializers.CharField(write_only=True, min_length=8, style={'input_type': 'password'})
    password_confirm = serializers.CharField(write_only=True, min_length=8, style={'input_type': 'password'})
    profesor_numero_empleado = serializers.CharField(
        required=False, 
        allow_blank=True,
        help_text='Número de empleado del profesor (solo para docentes)'
    )
    
    class Meta:
        model = CustomUser
        fields = [
            'username', 'password', 'password_confirm', 'email', 'role', 
            'first_name', 'last_name', 'profesor_numero_empleado'
        ]
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }
    
    def validate(self, data):
        # Validaciones personalizadas
        # Verificar que las contraseñas coincidan
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({"password": "Las contraseñas no coinciden."})
        
        # Si es docente, debe proporcionar número de empleado
        if data.get('role') == CustomUser.DOCENTE and not data.get('profesor_numero_empleado'):
            raise serializers.ValidationError({
                "profesor_numero_empleado": "Los docentes deben proporcionar su número de empleado."
            })
        
        # Verificar que el profesor existe si se proporciona número de empleado
        if data.get('profesor_numero_empleado'):
            try:
                profesor = Profesor.objects.get(numero_empleado=data['profesor_numero_empleado'])
                # Verificar que el profesor no tenga ya un usuario asignado
                if profesor.user is not None:
                    raise serializers.ValidationError({
                        "profesor_numero_empleado": "Este profesor ya tiene un usuario asignado."
                    })
                data['profesor'] = profesor
            except Profesor.DoesNotExist:
                raise serializers.ValidationError({
                    "profesor_numero_empleado": "No existe un profesor con este número de empleado."
                })
        
        return data
    
    def create(self, validated_data):
        # Crear usuario y vincular con profesor si aplica
        # Remover campos que no son del modelo User
        validated_data.pop('password_confirm')
        profesor = validated_data.pop('profesor', None)
        validated_data.pop('profesor_numero_empleado', None)
        
        # Crear el usuario
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
            role=validated_data.get('role', CustomUser.DOCENTE),
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        
        # Vincular con profesor si es docente
        if profesor:
            profesor.user = user
            profesor.save()
        
        return user

class UserUpdateSerializer(serializers.ModelSerializer):
    # Serializer para actualizar datos del usuario
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name']
    
    def validate_email(self, value):
        """Validar que el email no esté en uso por otro usuario"""
        user = self.context['request'].user
        if CustomUser.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError("Este email ya está en uso.")
        return value

class ChangePasswordSerializer(serializers.Serializer):
    # Serializer para cambio de contraseña
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True, min_length=8)
    new_password_confirm = serializers.CharField(required=True, write_only=True, min_length=8)
    
    def validate(self, data):
        if data['new_password'] != data['new_password_confirm']:
            raise serializers.ValidationError({"new_password": "Las contraseñas no coinciden."})
        return data
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("La contraseña actual es incorrecta.")
        return value
    
    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user
```
###tests.py
<p>
Esta clase sirve para importar los testsCase.
</p>

```python
from django.test import TestCase

# Create your tests here.
```
###urls.py
<p>
Esta clase sirve para crear las los links de las vistas.
</p>

```python
from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from usuarios_y_acceso.views import (
    RegisterView,
    UserProfileView,
    ChangePasswordView,
    UserListView,
)

app_name = 'usuarios_y_acceso'

urlpatterns = [
    # Autenticación
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Perfil de usuario
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    
    # Administración de usuarios (solo admins)
    path('users/', UserListView.as_view(), name='user_list'),
]
```
###views.py
<p>
Esta clase sirve para crear las vistas y mandar los datos del front-end a la base de datos.
</p>

```python
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from usuarios_y_acceso.serializers import (
    UserRegisterSerializer, 
    UserSerializer, 
    UserUpdateSerializer,
    ChangePasswordSerializer
)

from usuarios_y_acceso.models import CustomUser
from usuarios_y_acceso.permissions import IsAdmin

# Create your views here.
class RegisterView(generics.CreateAPIView):
    """
    Vista para registro de nuevos usuarios
    Abierta al público o puede ser restringida a admins según necesites
    """
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)  # Cambiar a (IsAdmin,) si solo admins pueden registrar
    serializer_class = UserRegisterSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        return Response({
            'message': 'Usuario registrado exitosamente',
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)

class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    Vista para ver y actualizar el perfil del usuario actual
    GET: Ver perfil completo
    PUT/PATCH: Actualizar datos básicos
    """
    permission_classes = (IsAuthenticated,)
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return UserUpdateSerializer
        return UserSerializer
    
    def get_object(self):
        return self.request.user

class ChangePasswordView(APIView):
    """
    Vista para cambiar la contraseña del usuario actual
    POST: Cambiar contraseña
    """
    permission_classes = (IsAuthenticated,)
    
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Contraseña actualizada exitosamente'
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserListView(generics.ListAPIView):
    """
    Vista para listar todos los usuarios (solo para admins)
    GET: Lista de usuarios con filtros
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # Filtros opcionales
        role = self.request.query_params.get('role', None)
        if role:
            queryset = queryset.filter(role=role)
        return queryset::
```
