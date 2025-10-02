from rest_framework import serializers

from core.serializers import CursoSerializer
from evaluacion_acreditacion.models import AccionMejora, AportacionPE, EvaluacionIndicador, GestionAcademica, Hallazgo, Indicador, Auditoria

class AccionMejoraSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccionMejora
        fields = ['accion_id', 'hallazgo_id', 'descripcion', 'resultado_esperado', 'meta', 'fecha_meta', 'responsable', 'estatus']
        read_only_fields = ['accion_id']

class EvaluacionIndicadorSerializer(serializers.ModelSerializer):
    curso = CursoSerializer(read_only=True, source='curso_id')
    
    class Meta:
        model = EvaluacionIndicador
        fields = ['evaluacion_id', 'indicador_id', 'curso_id', 'grupo_seccion', 'instrumento_evaluacion', 'descripcion_instrumento', 'periodo_evaluacion', 'valoracion', 'analisis_resultados', 'meta', 'curso']
        read_only_fields = ['evaluacion_id', 'curso']

class IndicadorSerializer(serializers.ModelSerializer):
    evaluaciones = EvaluacionIndicadorSerializer(many=True, read_only=True)
    
    class Meta:
        model = Indicador
        fields = ['indicador_id', 'criterio_id', 'codigo', 'descripcion', 'evaluaciones']
        read_only_fields = ['indicador_id']

class AportacionPESerializer(serializers.ModelSerializer):
    class Meta:
        model = AportacionPE
        fields = ['aportacion_id', 'profesor_id', 'descripcion']
        read_only_fields = ['aportacion_id']

class GestionAcademicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = GestionAcademica
        fields = ['gestion_id', 'profesor_id', 'actividad', 'institucion', 'fecha_inicio', 'fecha_fin']
        read_only_fields = ['gestion_id']

class HallazgoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hallazgo
        fields = ['hallazgo_id', 'programa_id', 'numero_hallazgo', 'descripcion', 'objetivo_id', 'atributo_pe_id', 'es_indice_rendimiento', 'indicador_mr2025']
        read_only_fields = ['hallazgo_id']

class AuditoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auditoria
        fields = ['auditoria_id', 'accion', 'tabla_afectada', 'registro_id', 'datos_anteriores', 'datos_nuevos', 'ip_address', 'user_agent']
        read_only_fields = ['auditoria_id']
