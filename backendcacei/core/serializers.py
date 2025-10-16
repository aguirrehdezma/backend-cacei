from rest_framework import serializers

from core.models import Curso, Institucion, Organizacion, Profesor, ProgramaEducativo


class ProfesorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profesor
        fields = ['profesor_id', 'numero_empleado', 'apellido_paterno', 'apellido_materno', 'nombres', 'fecha_nacimiento', 'nombramiento_actual', 'antiguedad', 'experiencia_ingenieria']
        read_only_fields = ['profesor_id']

class ProgramaEducativoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramaEducativo
        fields = ['programa_id', 'clave', 'nombre', 'descripcion', 'fecha_creacion', 'estatus']
        read_only_fields = ['programa_id']

class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = ['curso_id', 'programa_id', 'clave', 'nombre', 'seriacion', 'ubicacion', 'tipo', 'horas_totales', 'objetivo_general']
        read_only_fields = ['curso_id']

class InstitucionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institucion
        fields = ['institucion_id', 'nombre']
        read_only_fields = ['institucion_id']

class OrganizacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organizacion
        fields = ['organizacion_id', 'nombre']
        read_only_fields = ['organizacion_id']
