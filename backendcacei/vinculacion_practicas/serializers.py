from rest_framework import serializers
from .models import Practica

class PracticaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Practica
        fields = ['practica_id', 'curso_id', 'numero', 'descripcion', 'created_at', 'updated_at']
        read_only_fields = ['practica_id', 'created_at', 'updated_at']