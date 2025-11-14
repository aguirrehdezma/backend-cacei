from django.db import models

# Create your models here.
class Cedula(models.Model):
    ORGANIZACION_CURRICULAR = 'organizacion_curricular'
    CV_SINTETICO = 'cv_sintetico'
    PLAN_MEJORA = 'plan_mejora'
    VALORACION_OBJETIVOS = 'valoracion_objetivos'
    AEP_VS_AECACEI = 'aep_vs_aecacei'
    AEP_VS_OE = 'aep_vs_oe'

    TIPO_CHOICES = [
        (ORGANIZACION_CURRICULAR, 'Organización Curricular'),
        (CV_SINTETICO, 'CV Sintético'),
        (PLAN_MEJORA, 'Plan de Mejora'),
        (VALORACION_OBJETIVOS, 'Valoración de Objetivos'),
        (AEP_VS_AECACEI, 'AEP vs AE-CACEI'),
        (AEP_VS_OE, 'AEP vs OE'),
    ]
    
    programa = models.ForeignKey('core.ProgramaEducativo', on_delete=models.PROTECT, null=True, blank=True)
    periodo = models.ForeignKey('core.Periodo', on_delete=models.PROTECT, null=True, blank=True)
    profesor = models.ForeignKey('core.Profesor', on_delete=models.PROTECT, null=True, blank=True)
    
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
    
    def __str__(self):
        return f"Cédula {self.tipo} - {self.id}"

# ORGANIZACION CURRICULAR MODELS

class CursoObligatorio(models.Model):
    cedula = models.ForeignKey(Cedula, on_delete=models.PROTECT)
    curso = models.ForeignKey('core.Curso', on_delete=models.PROTECT)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.curso.nombre} (Obligatorio)"

class CursoOptativo(models.Model):
    cedula = models.ForeignKey(Cedula, on_delete=models.PROTECT)
    curso = models.ForeignKey('core.Curso', on_delete=models.PROTECT)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.curso.nombre} (Optativo)"

# CV SINTETICO MODELS

class ActualizacionDisciplinarCedula(models.Model):
    cedula = models.ForeignKey(Cedula, on_delete=models.PROTECT)
    actualizacion = models.ForeignKey('gestion_de_profesores.ActualizacionDisciplinar', on_delete=models.PROTECT)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class FormacionAcademicaCedula(models.Model):
    cedula = models.ForeignKey(Cedula, on_delete=models.PROTECT)
    formacion = models.ForeignKey('gestion_de_profesores.FormacionAcademica', on_delete=models.PROTECT)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CapacitacionDocenteCedula(models.Model):
    cedula = models.ForeignKey(Cedula, on_delete=models.PROTECT)
    capacitacion = models.ForeignKey('gestion_de_profesores.CapacitacionDocente', on_delete=models.PROTECT)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ExperienciaProfesionalCedula(models.Model):
    cedula = models.ForeignKey(Cedula, on_delete=models.PROTECT)
    experiencia = models.ForeignKey('gestion_de_profesores.ExperienciaProfesional', on_delete=models.PROTECT)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ExperienciaDisenoCedula(models.Model):
    cedula = models.ForeignKey(Cedula, on_delete=models.PROTECT)
    experiencia = models.ForeignKey('gestion_de_profesores.ExperienciaDiseno', on_delete=models.PROTECT)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class LogroProfesionalCedula(models.Model):
    cedula = models.ForeignKey(Cedula, on_delete=models.PROTECT)
    logro = models.ForeignKey('gestion_de_profesores.LogroProfesional', on_delete=models.PROTECT)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ParticipacionOrganizacionesCedula(models.Model):
    cedula = models.ForeignKey(Cedula, on_delete=models.PROTECT)
    participacion = models.ForeignKey('gestion_de_profesores.ParticipacionOrganizaciones', on_delete=models.PROTECT)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class PremioDistincionCedula(models.Model):
    cedula = models.ForeignKey(Cedula, on_delete=models.PROTECT)
    premio = models.ForeignKey('gestion_de_profesores.PremioDistincion', on_delete=models.PROTECT)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ProductoAcademicoCedula(models.Model):
    cedula = models.ForeignKey(Cedula, on_delete=models.PROTECT)
    producto = models.ForeignKey('gestion_de_profesores.ProductoAcademico', on_delete=models.PROTECT)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class AportacionPECedula(models.Model):
    cedula = models.ForeignKey(Cedula, on_delete=models.PROTECT)
    aportacion = models.ForeignKey('evaluacion_acreditacion.AportacionPE', on_delete=models.PROTECT)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class GestionAcademicaCedula(models.Model):
    cedula = models.ForeignKey(Cedula, on_delete=models.PROTECT)
    gestion = models.ForeignKey('evaluacion_acreditacion.GestionAcademica', on_delete=models.PROTECT)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# PLAN DE MEJORA MODELS

class HallazgoCedula(models.Model):
    cedula = models.ForeignKey(Cedula, on_delete=models.PROTECT)
    hallazgo = models.ForeignKey('evaluacion_acreditacion.Hallazgo', on_delete=models.PROTECT)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class AccionMejoraCedula(models.Model):
    cedula = models.ForeignKey(Cedula, on_delete=models.PROTECT)
    hallazgo = models.ForeignKey('evaluacion_acreditacion.Hallazgo', on_delete=models.PROTECT)
    accion = models.ForeignKey('evaluacion_acreditacion.AccionMejora', on_delete=models.PROTECT)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# VALORACION DE OBJETIVOS MODELS

class ObjetivoEducacionalCedula(models.Model):
    cedula = models.ForeignKey(Cedula, on_delete=models.PROTECT)
    objetivo = models.ForeignKey('gestion_academica.ObjetivoEducacional', on_delete=models.PROTECT)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class AtributoObjetivoCedula(models.Model):
    cedula = models.ForeignKey(Cedula, on_delete=models.PROTECT)
    objetivo = models.ForeignKey('gestion_academica.ObjetivoEducacional', on_delete=models.PROTECT)
    atributo = models.ForeignKey('gestion_academica.AtributoPE', on_delete=models.PROTECT)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CriterioDesempenoCedula(models.Model):
    cedula = models.ForeignKey(Cedula, on_delete=models.PROTECT)
    atributo = models.ForeignKey('gestion_academica.AtributoPE', on_delete=models.PROTECT)
    criterio = models.ForeignKey('gestion_academica.CriterioDesempeno', on_delete=models.PROTECT)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class IndicadorCedula(models.Model):
    cedula = models.ForeignKey(Cedula, on_delete=models.PROTECT)
    criterio = models.ForeignKey('gestion_academica.CriterioDesempeno', on_delete=models.PROTECT)
    indicador = models.ForeignKey('evaluacion_acreditacion.Indicador', on_delete=models.PROTECT)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class EvaluacionIndicadorCedula(models.Model):
    cedula = models.ForeignKey(Cedula, on_delete=models.PROTECT)
    indicador = models.ForeignKey('evaluacion_acreditacion.Indicador', on_delete=models.PROTECT)
    evaluacion = models.ForeignKey('evaluacion_acreditacion.EvaluacionIndicador', on_delete=models.PROTECT)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# AEP vs AE-CACEI MODELS

class AtributoPECedula(models.Model):
    cedula = models.ForeignKey(Cedula, on_delete=models.PROTECT)
    atributo_pe = models.ForeignKey('gestion_academica.AtributoPE', on_delete=models.PROTECT)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class AtributoPECACEICedula(models.Model):
    cedula = models.ForeignKey(Cedula, on_delete=models.PROTECT)
    atributo_pe = models.ForeignKey('gestion_academica.AtributoPE', on_delete=models.PROTECT)
    atributo_cacei = models.ForeignKey('gestion_academica.AtributoCACEI', on_delete=models.PROTECT)
    relacion = models.ForeignKey('gestion_academica.AtributoPECACEI', on_delete=models.PROTECT)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# AEP vs OE MODELS

class AtributoObjetivoCedulaAEPVsOE(models.Model):
    cedula = models.ForeignKey(Cedula, on_delete=models.PROTECT)
    objetivo = models.ForeignKey('gestion_academica.ObjetivoEducacional', on_delete=models.PROTECT)
    atributo_pe = models.ForeignKey('gestion_academica.AtributoPE', on_delete=models.PROTECT)
    relacion = models.ForeignKey('gestion_academica.AtributoPEObjetivo', on_delete=models.PROTECT)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
