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
    curso_ejes = serializers.SerializerMethodField()
    curso_atributos_pe = serializers.SerializerMethodField()
    
    class Meta:
        model = Curso
        fields = ['curso_id', 'programa_id', 'clave', 'nombre', 'seriacion', 'ubicacion', 'tipo', 'horas_totales', 'objetivo_general', 'curso_ejes', 'curso_atributos_pe']
        read_only_fields = ['curso_id']
    
    def get_curso_ejes(self, obj):
        from gestion_academica.serializers import CursoEjeSerializer
        curso_ejes = obj.curso_eje.all()
        return CursoEjeSerializer(curso_ejes, many=True).data
    
    def get_curso_atributos_pe(self, obj):
        from gestion_academica.serializers import CursoAtributoPESerializer
        curso_atributos_pe = obj.curso_atributo_pe.all()
        return CursoAtributoPESerializer(curso_atributos_pe, many=True).data

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
