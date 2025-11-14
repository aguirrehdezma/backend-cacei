from rest_framework import serializers

from gestion_academica.serializers import AtributoCACEISerializer, AtributoPECACEISerializer, AtributoPESerializer, CriterioDesempenoSerializer, ObjetivoEducacionalSerializer
from cedulas.models import AccionMejoraCedula, ActualizacionDisciplinarCedula, AportacionPECedula, AtributoObjetivoCedula, AtributoPECACEICedula, AtributoPECedula, CapacitacionDocenteCedula, Cedula, CriterioDesempenoCedula, CursoObligatorio, CursoOptativo, EvaluacionIndicadorCedula, ExperienciaDisenoCedula, ExperienciaProfesionalCedula, FormacionAcademicaCedula, GestionAcademicaCedula, HallazgoCedula, IndicadorCedula, LogroProfesionalCedula, ObjetivoEducacionalCedula, ParticipacionOrganizacionesCedula, PremioDistincionCedula, ProductoAcademicoCedula
from core.models import Periodo, Profesor, ProgramaEducativo

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

    class Meta:
        model = Cedula
        fields = [
            "id", "programa", "programa_id", "periodo", "periodo_id", "tipo",
            "cursos_obligatorios",
            "cursos_optativos",
        ]
        read_only_fields = ["id"]
    
    def get_cursos_obligatorios(self, obj):
        relaciones = CursoObligatorio.objects.filter(cedula=obj)
        return CursoObligatorioSerializer(relaciones, many=True).data

    def get_cursos_optativos(self, obj):
        relaciones = CursoOptativo.objects.filter(cedula=obj)
        return CursoOptativoSerializer(relaciones, many=True).data

class CursoOptativoSerializer(serializers.ModelSerializer):
    curso = CursoSerializer(read_only=True)

    class Meta:
        model = CursoOptativo
        fields = ["id", "curso"]

class CursoObligatorioSerializer(serializers.ModelSerializer):
    curso = CursoSerializer(read_only=True)
    
    class Meta:
        model = CursoObligatorio
        fields = ["id", "curso"]

class CedulaCvSinteticoSerializer(serializers.ModelSerializer):
    profesor = ProfesorSerializer(read_only=True)
    profesor_id = serializers.PrimaryKeyRelatedField(
        queryset=Profesor.objects.all(), source='profesor', write_only=True
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
            "id", "tipo", "profesor", "profesor_id",
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
    
    class Meta:
        model = EvaluacionIndicadorCedula
        fields = ["id", "evaluacion"]

class IndicadorCedulaSerializer(serializers.ModelSerializer):
    indicador = IndicadorSerializer(read_only=True)
    evaluaciones = serializers.SerializerMethodField()
    
    class Meta:
        model = IndicadorCedula
        fields = ["id", "indicador", "evaluaciones"]
        
    def get_evaluaciones(self, obj):
        relaciones = EvaluacionIndicadorCedula.objects.filter(cedula=obj.cedula, indicador=obj.indicador)
        return EvaluacionIndicadorCedulaSerializer(relaciones, many=True).data

class CriterioCedulaSerializer(serializers.ModelSerializer):
    criterio = CriterioDesempenoSerializer(read_only=True)
    indicadores = serializers.SerializerMethodField()
    
    class Meta:
        model = CriterioDesempenoCedula
        fields = ["id", "criterio", "indicadores"]
        
    def get_indicadores(self, obj):
        relaciones = IndicadorCedula.objects.filter(cedula=obj.cedula, criterio=obj.criterio)
        return IndicadorCedulaSerializer(relaciones, many=True).data

class AtributoObjetivoCedulaSerializer(serializers.ModelSerializer):
    atributo = AtributoPESerializer(read_only=True)
    criterios = serializers.SerializerMethodField()
    
    class Meta:
        model = AtributoObjetivoCedula
        fields = ["id", "atributo", "criterios"]
    
    def get_criterios(self, obj):
        relaciones = CriterioDesempenoCedula.objects.filter(cedula=obj.cedula, atributo=obj.atributo)
        return CriterioCedulaSerializer(relaciones, many=True).data

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
