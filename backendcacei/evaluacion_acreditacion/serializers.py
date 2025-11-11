from rest_framework import serializers

from evaluacion_acreditacion.models import AccionMejora, AportacionPE, EvaluacionIndicador, GestionAcademica, Hallazgo, Indicador, Auditoria

class AccionMejoraSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccionMejora
        fields = ['id', 'hallazgo', 'descripcion', 'resultado_esperado', 'meta', 'fecha_meta', 'responsable', 'estatus']
        read_only_fields = ['id']

class EvaluacionIndicadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvaluacionIndicador
        fields = ['id', 'indicador', 'curso', 'grupo_seccion', 'instrumento_evaluacion', 'descripcion_instrumento', 'periodo_evaluacion', 'valoracion', 'analisis_resultados', 'meta']
        read_only_fields = ['id']

class IndicadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Indicador
        fields = ['id', 'criterio', 'codigo', 'descripcion']
        read_only_fields = ['id']

class AportacionPESerializer(serializers.ModelSerializer):
    class Meta:
        model = AportacionPE
        fields = ['id', 'profesor', 'descripcion']
        read_only_fields = ['id']

class GestionAcademicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = GestionAcademica
        fields = ['id', 'profesor', 'institucion', 'actividad', 'fecha_inicio', 'fecha_fin']
        read_only_fields = ['id']

class HallazgoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hallazgo
        fields = ['id', 'programa', 'numero_hallazgo', 'descripcion', 'objetivo', 'atributo_pe', 'es_indice_rendimiento', 'indicador_mr2025']
        read_only_fields = ['id']

class AuditoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auditoria
        fields = ['id', 'accion', 'tabla_afectada', 'registro_id', 'datos_anteriores', 'datos_nuevos', 'ip_address', 'user_agent']
        read_only_fields = ['id']