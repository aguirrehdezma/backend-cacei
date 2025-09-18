from rest_framework import serializers

from gestion_academica.models import CriterioDesempeno, Curso, EstrategiaEnsenanza, EstrategiaEvaluacion, ProgramaEducativo, UnidadTematica

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

class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = ['curso_id', 'clave', 'nombre', 'seriacion', 'ubicacion', 'tipo', 'horas_totales', 'objetivo_general']
        read_only_fields = ['curso_id']

class EstrategiaEnsenanzaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstrategiaEnsenanza
        fields = ['estrategia_id', 'numero', 'descripcion']
        read_only_fields = ['estrategia_id']

class EstrategiaEvaluacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstrategiaEvaluacion
        fields = ['estrategia_id', 'numero', 'descripcion']
        read_only_fields = ['estrategia_id']
