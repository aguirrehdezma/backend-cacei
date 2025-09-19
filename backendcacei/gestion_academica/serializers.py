from rest_framework import serializers

from gestion_academica.models import Bibliografia, CriterioDesempeno, Curso, EstrategiaEnsenanza, EstrategiaEvaluacion, HorasSemana, ObjetivoEducacional, ProductoAcademico, ProgramaEducativo, UnidadTematica

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

class ObjetivoEducacionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObjetivoEducacional
        fields = ['objetivo_id', 'codigo', 'descripcion']
        read_only_fields = ['objetivo_id']

class BibliografiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bibliografia
        fields = ['bibliografia_id', 'numero', 'autor', 'titulo', 'editorial', 'anio_publicacion']
        read_only_fields = ['bibliografia_id']

class HorasSemanaSerializer(serializers.ModelSerializer):
    class Meta:
        model = HorasSemana
        fields = ['horas_id', 'horas_totales', 'horas_aula', 'horas_laboratorio', 'horas_practicas', 'numero_grupos', 'calificacion_promedio', 'porcentaje_aprobacion', 'porcentaje_reprobacion']
        read_only_fields = ['horas_id']

class ProductoAcademicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductoAcademico
        fields = ['producto_id', 'descripcion', 'anio', 'tipo', 'detalles']
        read_only_fields = ['producto_id']
