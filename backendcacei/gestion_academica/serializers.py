from rest_framework import serializers

from gestion_academica.models import CriterioDesempeno, ProgramaEducativo, UnidadTematica

class ProgramaEducativoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramaEducativo
        fields = ['programa_id', 'clave', 'nombre', 'descripcion', 'fecha_creacion', 'estatus']
        read_only_fields = ['programa_id', 'fecha_creacion']

class UnidadTematicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnidadTematica
        fields = ['unidad_id', 'numero', 'descripcion']
        read_only_fields = ['unidad_id']

class CriterioDesempenoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CriterioDesempeno
        fields = ['criterio_id', 'codigo', 'descripcion']
        read_only_fields = ['criterio_id']
