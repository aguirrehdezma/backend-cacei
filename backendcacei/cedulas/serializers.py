from rest_framework import serializers

from cedulas.models import ActualizacionDisciplinarCedula, AportacionPECedula, CapacitacionDocenteCedula, Cedula, CursoObligatorio, CursoOptativo, ExperienciaDisenoCedula, ExperienciaProfesionalCedula, FormacionAcademicaCedula, GestionAcademicaCedula, LogroProfesionalCedula, ParticipacionOrganizacionesCedula, PremioDistincionCedula, ProductoAcademicoCedula
from core.models import Periodo, Profesor, ProgramaEducativo

from gestion_de_profesores.serializers import ActualizacionDisciplinarSerializer, CapacitacionDocenteSerializer, ExperienciaDisenoSerializer, ExperienciaProfesionalSerializer, FormacionAcademicaSerializer, LogroProfesionalSerializer, ParticipacionOrganizacionesSerializer, PremioDistincionSerializer, ProductoAcademicoSerializer
from core.serializers import CursoSerializer, PeriodoSerializer, ProgramaEducativoSerializer, ProfesorSerializer
from evaluacion_acreditacion.serializers import AportacionPESerializer, GestionAcademicaSerializer

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
        read_only_fields = ["id"]

class CursoObligatorioSerializer(serializers.ModelSerializer):
    curso = CursoSerializer(read_only=True)
    
    class Meta:
        model = CursoObligatorio
        fields = ["id", "curso"]
        read_only_fields = ["id"]

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
        read_only_fields = ["id"]

class FormacionAcademicaCedulaSerializer(serializers.ModelSerializer):
    formacion = FormacionAcademicaSerializer(read_only=True)

    class Meta:
        model = FormacionAcademicaCedula
        fields = ["id", "formacion"]
        read_only_fields = ["id"]

class CapacitacionDocenteCedulaSerializer(serializers.ModelSerializer):
    capacitacion = CapacitacionDocenteSerializer(read_only=True)

    class Meta:
        model = CapacitacionDocenteCedula
        fields = ["id", "capacitacion"]
        read_only_fields = ["id"]

class ExperienciaProfesionalCedulaSerializer(serializers.ModelSerializer):
    experiencia = ExperienciaProfesionalSerializer(read_only=True)

    class Meta:
        model = ExperienciaProfesionalCedula
        fields = ["id", "experiencia"]
        read_only_fields = ["id"]

class ExperienciaDisenoCedulaSerializer(serializers.ModelSerializer):
    experiencia = ExperienciaDisenoSerializer(read_only=True)

    class Meta:
        model = ExperienciaDisenoCedula
        fields = ["id", "experiencia"]
        read_only_fields = ["id"]

class LogroProfesionalCedulaSerializer(serializers.ModelSerializer):
    logro = LogroProfesionalSerializer(read_only=True)

    class Meta:
        model = LogroProfesionalCedula
        fields = ["id", "logro"]
        read_only_fields = ["id"]

class ParticipacionOrganizacionesCedulaSerializer(serializers.ModelSerializer):
    participacion = ParticipacionOrganizacionesSerializer(read_only=True)

    class Meta:
        model = ParticipacionOrganizacionesCedula
        fields = ["id", "participacion"]
        read_only_fields = ["id"]

class PremioDistincionCedulaSerializer(serializers.ModelSerializer):
    premio = PremioDistincionSerializer(read_only=True)

    class Meta:
        model = PremioDistincionCedula
        fields = ["id", "premio"]
        read_only_fields = ["id"]

class ProductoAcademicoCedulaSerializer(serializers.ModelSerializer):
    producto = ProductoAcademicoSerializer(read_only=True)

    class Meta:
        model = ProductoAcademicoCedula
        fields = ["id", "producto"]
        read_only_fields = ["id"]

class AportacionPECedulaSerializer(serializers.ModelSerializer):
    aportacion = AportacionPESerializer(read_only=True)

    class Meta:
        model = AportacionPECedula
        fields = ["id", "aportacion"]
        read_only_fields = ["id"]

class GestionAcademicaCedulaSerializer(serializers.ModelSerializer):
    gestion = GestionAcademicaSerializer(read_only=True)

    class Meta:
        model = GestionAcademicaCedula
        fields = ["id", "gestion"]
        read_only_fields = ["id"]
