from rest_framework import serializers

from programas_educativos.models import ProgramaEducativo

class ProgramaEducativoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramaEducativo
        fields = ['programa_id', 'clave', 'nombre', 'descripcion', 'fecha_creacion', 'estatus']
        read_only_fields = ['programa_id', 'fecha_creacion']
