from rest_framework import serializers

from unidades_tematicas.models import UnidadTematica

class UnidadTematicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnidadTematica
        fields = ['unidad_id', 'numero', 'descripcion']
        read_only_fields = ['unidad_id']
