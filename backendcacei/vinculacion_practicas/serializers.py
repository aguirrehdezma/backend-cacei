from rest_framework import serializers

from vinculacion_practicas.models import Practica

class PracticaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Practica
        fields = ['practica_id', 'numero', 'descripcion']
        read_only_fields = ['practica_id']
