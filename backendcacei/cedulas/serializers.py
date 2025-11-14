from rest_framework import serializers

from cedulas.models import Cedula, CursoObligatorio, CursoOptativo
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
        fields = [
            "id", "curso",
        ]
        read_only_fields = ["id"]

class CursoObligatorioSerializer(serializers.ModelSerializer):
    curso = CursoSerializer(read_only=True)
    
    class Meta:
        model = CursoObligatorio
        fields = [
            "id", "curso",
        ]
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
        if obj.profesor is None:
            return []
        return ActualizacionDisciplinarSerializer(obj.profesor.actualizaciondisciplinar_set.all(), many=True).data
    
    def get_formaciones(self, obj):
        if obj.profesor is None:
            return []
        return FormacionAcademicaSerializer(obj.profesor.formacionacademica_set.all(), many=True).data
    
    def get_capacitaciones(self, obj):
        if obj.profesor is None:
            return []
        return CapacitacionDocenteSerializer(obj.profesor.capacitaciondocente_set.all(), many=True).data
    
    def get_experiencias(self, obj):
        if obj.profesor is None:
            return []
        return ExperienciaDisenoSerializer(obj.profesor.experienciadiseno_set.all(), many=True).data
    
    def get_disenos(self, obj):
        if obj.profesor is None:
            return []
        return ExperienciaDisenoSerializer(obj.profesor.experienciadiseno_set.all(), many=True).data
    
    def get_logros(self, obj):   
        if obj.profesor is None:
            return []
        return LogroProfesionalSerializer(obj.profesor.logroprofesional_set.all(), many=True).data
    
    def get_participaciones(self, obj):
        if obj.profesor is None:
            return []
        return ParticipacionOrganizacionesSerializer(obj.profesor.participacionorganizaciones_set.all(), many=True).data
    
    def get_premios(self, obj):
        if obj.profesor is None:
            return []
        return PremioDistincionSerializer(obj.profesor.premiodistincion_set.all(), many=True).data
    
    def get_productos(self, obj):
        if obj.profesor is None:
            return []
        return ProductoAcademicoSerializer(obj.profesor.productoacademico_set.all(), many=True).data
    
    def get_aportaciones_pe(self, obj):
        if obj.profesor is None:
            return []
        return AportacionPESerializer(obj.profesor.aportacionpe_set.all(), many=True).data
    
    def get_gestiones(self, obj):
        if obj.profesor is None:
            return []
        return GestionAcademicaSerializer(obj.profesor.gestionacademica_set.all(), many=True).data
