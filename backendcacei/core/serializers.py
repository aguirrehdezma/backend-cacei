from rest_framework import serializers

from core.models import Curso, Institucion, Organizacion, Periodo, Profesor, ProgramaEducativo

class ProfesorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profesor
        fields = ['id', 'numero_empleado', 'apellido_paterno', 'apellido_materno', 'nombres', 'fecha_nacimiento', 'nombramiento_actual', 'antiguedad', 'experiencia_ingenieria']
        read_only_fields = ['id']

class ProgramaEducativoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramaEducativo
        fields = ['id', 'clave', 'nombre', 'descripcion', 'fecha_creacion', 'estatus']
        read_only_fields = ['id']

class CursoSerializer(serializers.ModelSerializer):
    curso_ejes = serializers.SerializerMethodField()
    curso_atributos_pe = serializers.SerializerMethodField()
    
    class Meta:
        model = Curso
        fields = ['id', 'programa', 'clave', 'nombre', 'seriacion', 'ubicacion', 'tipo', 'horas_totales', 'objetivo_general', 'curso_ejes', 'curso_atributos_pe']
        read_only_fields = ['id']
    
    def get_curso_ejes(self, obj):
        from gestion_academica.serializers import CursoEjeSerializer
        curso_ejes = obj.cursoeje_set.all()
        return CursoEjeSerializer(curso_ejes, many=True).data
    
    def get_curso_atributos_pe(self, obj):
        from gestion_academica.serializers import CursoAtributoPESerializer
        curso_atributos_pe = obj.cursoatributope_set.all()
        return CursoAtributoPESerializer(curso_atributos_pe, many=True).data

class InstitucionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institucion
        fields = ['id', 'nombre']
        read_only_fields = ['id']

class OrganizacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organizacion
        fields = ['id', 'nombre']
        read_only_fields = ['id']

class PeriodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Periodo
        fields = ['id', 'nombre', 'fecha_inicio', 'fecha_fin']
        read_only_fields = ['id']