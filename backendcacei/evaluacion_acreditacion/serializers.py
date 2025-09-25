from rest_framework import serializers
from .models import AccionMejora, Gestion_Academica
from .models import Indicador
from .models import Evaluacion_Indicador
from .models import aportacion_pe
from .models import Hallazgo
from .models import Auditoria

class AccionMejoraSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccionMejora
        fields = ['accion_id','descripcion', 'resultado_esperado', 'meta', 'fecha_meta', 'responsable', 'estatus']
        read_only_fields = ['accion_id']


class IndicadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Indicador
        fields = ['indicador_id', 'codigo', 'descripcion']
        read_only_fields = ['indicador_id']
    

class EvaluacionIndicadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluacion_Indicador
        fields = ['evaluacion_id', 'grupo_seccion', 'instrumento_evaluacion', 'descripcion_instrumento', 'periodo_evaluacion', 'valoracion', 'analisis_resultados', 'meta']
        read_only_fields = ['evaluacion_id']

class AportacionPESerializer(serializers.ModelSerializer):
    class Meta:
        model = aportacion_pe
        fields = ['aportacion_id', 'descripcion']
        read_only_fields = ['aportacion_id']


class GestionAcademicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gestion_Academica
        fields = ['gestion_id', 'actividad', 'institucion', 'fecha_inicio', 'fecha_fin']
        read_only_fields = ['gestion_id']


class HallazgoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hallazgo
        fields = ['hallazgo_id','numero_hallazgo', 'descripcion', 'objetivo_id', 'atributo_pe_id', 'es_indice_rendimiento', 'indicador_mr2025']
        read_only_fields = ['hallazgo_id']


class AuditoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auditoria
        fields = ['auditoria_id','usuario_id','accion','tabla_afectada','registro_id','datos_anteriores','datos_nuevos','ip_address','user_agent']
        read_only_fields = ['Auditoria_id']

