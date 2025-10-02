from rest_framework import serializers

from gestion_academica.models import AtributoPE
from core.models import Profesor
from gestion_academica.serializers import AtributoPESerializer, CriterioDesempenoSerializer, ObjetivoEducacionalSerializer
from evaluacion_acreditacion.models import Hallazgo
from evaluacion_acreditacion.serializers import AccionMejoraSerializer, AportacionPESerializer, GestionAcademicaSerializer
from gestion_de_profesores.serializers import ActualizacionDisciplinarSerializer, CapacitacionDocenteSerializer, ExperienciaDisenoSerializer, ExperienciaProfesionalSerializer, FormacionAcademicaSerializer, LogroProfesionalSerializer, ParticipacionOrganizacionesSerializer, PremioDistincionSerializer

class CedulaCVSinteticoSerializer(serializers.ModelSerializer):
    formacion_academica = FormacionAcademicaSerializer(many=True, read_only=True)
    capacitacion_docente = CapacitacionDocenteSerializer(many=True, read_only=True)
    actualizacion_disciplinar = ActualizacionDisciplinarSerializer(many=True, read_only=True)
    gestion_academica = GestionAcademicaSerializer(many=True, read_only=True)
    experiencia_profesional = ExperienciaProfesionalSerializer(many=True, read_only=True)
    experiencia_diseno = ExperienciaDisenoSerializer(many=True, read_only=True)
    logros_profesionales = LogroProfesionalSerializer(many=True, read_only=True)
    participaciones_organizaciones = ParticipacionOrganizacionesSerializer(many=True, read_only=True)
    premios_distinciones = PremioDistincionSerializer(many=True, read_only=True)
    aportaciones_pe = AportacionPESerializer(many=True, read_only=True)

    edad = serializers.SerializerMethodField()
    
    class Meta:
        model = Profesor
        fields = [
            "numero_empleado", 
            "apellido_paterno", "apellido_materno", "nombres",
            "edad", "fecha_nacimiento", "nombramiento_actual", "antiguedad", 
            "formacion_academica", "capacitacion_docente", "actualizacion_disciplinar",
            "gestion_academica", "experiencia_profesional", "experiencia_diseno",
            "logros_profesionales", "participaciones_organizaciones", "premios_distinciones",
            "aportaciones_pe"
        ]
    
    def get_edad(self, obj):
        from datetime import date
        if obj.fecha_nacimiento:
            today = date.today()
            return today.year - obj.fecha_nacimiento.year - ((today.month, today.day) < (obj.fecha_nacimiento.month, obj.fecha_nacimiento.day))
        return None

class CedulaPlanMejoraSerializer(serializers.ModelSerializer):
    objetivo = ObjetivoEducacionalSerializer(read_only=True, source='objetivo_id')
    atributo_pe = AtributoPESerializer(read_only=True, source='atributo_pe_id')
    acciones_mejora = AccionMejoraSerializer(many=True, read_only=True)
    
    class Meta:
        model = Hallazgo
        fields = [
            "numero_hallazgo", "descripcion", "es_indice_rendimiento", "indicador_mr2025",
            "objetivo", "atributo_pe", "acciones_mejora"
        ]

class CedulaHerramientasValoracionAEPSerializer(serializers.ModelSerializer):
    criterios_desempeno = CriterioDesempenoSerializer(many=True, read_only=True)
    
    class Meta:
        model = AtributoPE
        fields = [
            "descripcion", 
            "criterios_desempeno"
        ]
