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
    curso = models.ForeignKey('core.Curso', on_delete=models.PROTECT, null=True, blank=True)
    
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
