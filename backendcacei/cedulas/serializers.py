from rest_framework import serializers

from evaluacion_acreditacion.serializers import AportacionPESerializer, GestionAcademicaSerializer
from gestion_de_profesores.serializers import ActualizacionDisciplinarSerializer, CapacitacionDocenteSerializer, ExperienciaDisenoSerializer, ExperienciaProfesionalSerializer, FormacionAcademicaSerializer, LogroProfesionalSerializer, ParticipacionOrganizacionesSerializer, PremioDistincionSerializer
from gestion_de_profesores.models import Profesor

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
        fields = ["numero_empleado", 
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
