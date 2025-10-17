from collections import defaultdict
from rest_framework import serializers

from gestion_academica.models import AtributoPE, ObjetivoEducacional
from core.models import Profesor, Curso, ProgramaEducativo
from evaluacion_acreditacion.models import Hallazgo

from gestion_academica.serializers import AtributoPEObjetivoSerializer, AtributoPESerializer, CriterioDesempenoSerializer, ObjetivoEducacionalSerializer, CursoAtributoPESerializer, HorasSemanaSerializer, UnidadTematicaSerializer, EstrategiaEnsenanzaSerializer, EstrategiaEvaluacionSerializer, PracticaSerializer, BibliografiaSerializer
from evaluacion_acreditacion.serializers import AccionMejoraSerializer, AportacionPESerializer, GestionAcademicaSerializer 
from gestion_de_profesores.serializers import ActualizacionDisciplinarSerializer, CapacitacionDocenteSerializer, ExperienciaDisenoSerializer, ExperienciaProfesionalSerializer, FormacionAcademicaSerializer, LogroProfesionalSerializer, ParticipacionOrganizacionesSerializer, PremioDistincionSerializer, ProductoAcademicoSerializer, ProfesorCursoSerializer 
from core.serializers import CursoSerializer

class CedulaCVSinteticoSerializer(serializers.ModelSerializer):
    formacion_academica = FormacionAcademicaSerializer(many=True, read_only=True)
    capacitacion_docente = CapacitacionDocenteSerializer(many=True, read_only=True)
    actualizacion_disciplinar = ActualizacionDisciplinarSerializer(many=True, read_only=True)
    gestion_academica = GestionAcademicaSerializer(many=True, read_only=True)
    producto_academico = ProductoAcademicoSerializer(many=True, read_only=True)
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
            "gestion_academica", "producto_academico", "experiencia_profesional", "experiencia_diseno",
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

class CedulaProgramaAsignaturaSerializer(serializers.ModelSerializer):
    curso_atributo_pe = CursoAtributoPESerializer(many=True, read_only=True)
    horas_semana = HorasSemanaSerializer(many=True, read_only=True)
    unidades_tematicas = UnidadTematicaSerializer(many=True, read_only=True)
    estrategias_ensenanza = EstrategiaEnsenanzaSerializer(many=True, read_only=True)
    estrategias_evaluacion = EstrategiaEvaluacionSerializer(many=True, read_only=True)
    practicas = PracticaSerializer(many=True, read_only=True)
    bibliografias = BibliografiaSerializer(many=True, read_only=True)
    profesores_cursos = ProfesorCursoSerializer(many=True, read_only=True)

    class Meta:
        model = Curso
        fields = [
            "clave", "nombre", "seriacion", "ubicacion", "tipo", "horas_totales", "objetivo_general",
            "curso_atributo_pe",
            "horas_semana",
            "unidades_tematicas",
            "estrategias_ensenanza",
            "estrategias_evaluacion",
            "practicas",
            "bibliografias",
            "profesores_cursos"
        ]

class CedulaValoracionOEPESerializer(serializers.ModelSerializer):
    atributo_pe_objetivo = AtributoPEObjetivoSerializer(many=True, read_only=True)
    
    class Meta:
        model = ObjetivoEducacional
        fields = [
            "descripcion",
            "atributo_pe_objetivo",
        ]

class CedulaOrganizacionCurricularSerializer(serializers.ModelSerializer):
    cursos_obligatorios = serializers.SerializerMethodField()
    cursos_optativos = serializers.SerializerMethodField()
    totales_por_eje = serializers.SerializerMethodField()

    class Meta:
        model = ProgramaEducativo
        fields = ['programa_id', 'cursos_obligatorios', 'cursos_optativos', 'totales_por_eje']

    def get_cursos_obligatorios(self, obj):
        cursos = obj.cursos.filter(tipo='obligatorio')
        return CursoSerializer(cursos, many=True).data

    def get_cursos_optativos(self, obj):
        cursos = obj.cursos.filter(tipo='optativo')
        return CursoSerializer(cursos, many=True).data

    def get_totales_por_eje(self, obj):
        totales_obligatorios = defaultdict(int)
        totales_optativos = defaultdict(int)
        totales = defaultdict(int)

        for curso in obj.cursos.all():
            for curso_eje in curso.curso_eje.all():
                eje_id = curso_eje.eje_id_id
                horas = curso_eje.horas
                if curso.tipo == 'obligatorio':
                    totales_obligatorios[eje_id] += horas
                else:
                    totales_optativos[eje_id] += horas
                totales[eje_id] += horas

        total_horas = sum(totales.values()) or 1

        porcentajes = [
            {
                "eje_id": eje_id,
                "porcentaje": round(horas / total_horas * 100, 2)
            }
            for eje_id, horas in totales.items()
        ]

        return {
            "obligatorios": [{
                "eje_id": eje_id,
                "horas": horas
            } for eje_id, horas in totales_obligatorios.items()],
            "optativos": [{
                "eje_id": eje_id,
                "horas": horas
            } for eje_id, horas in totales_optativos.items()],
            "totales": [{
                "eje_id": eje_id,
                "horas": horas
            } for eje_id, horas in totales.items()],
            "porcentajes": porcentajes
        }
