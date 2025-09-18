from rest_framework import serializers
from .models import AccionMejora
from .models import Indicador

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