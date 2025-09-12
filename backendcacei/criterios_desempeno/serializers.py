from rest_framework import serializers

from criterios_desempeno.models import CriterioDesempeno

class CriterioDesempenoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CriterioDesempeno
        fields = ['criterio_id', 'codigo', 'descripcion']
        read_only_fields = ['criterio_id']
