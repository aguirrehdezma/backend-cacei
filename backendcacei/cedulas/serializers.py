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
