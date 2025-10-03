from rest_framework import serializers

from core.serializers import ProfesorSerializer
from gestion_de_profesores.models import ActualizacionDisciplinar, CapacitacionDocente, ExperienciaDiseno, ExperienciaProfesional, FormacionAcademica, LogroProfesional, ParticipacionOrganizaciones, PremioDistincion, ProductoAcademico, ProfesorCurso

class ProfesorCursoSerializer(serializers.ModelSerializer):
    profesor = ProfesorSerializer(read_only=True, source='profesor_id')
    class Meta:
        model = ProfesorCurso
        fields = ['profesor_curso_id', 'profesor_id', 'curso_id', 'tipo', 'periodo', 'profesor']
        read_only_fields = ['profesor_curso_id']

class FormacionAcademicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormacionAcademica
        fields = ['formacion_id', 'profesor_id', 'nivel', 'institucion', 'pais', 'anio_obtencion', 'cedula_profesional', 'especialidad']
        read_only_fields = ['formacion_id']

class ExperienciaProfesionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExperienciaProfesional
        fields = ['experiencia_id', 'profesor_id', 'organizacion', 'puesto', 'fecha_inicio', 'fecha_fin', 'actividades']
        read_only_fields = ['experiencia_id']

class ExperienciaDisenoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExperienciaDiseno
        fields = ['diseno_id', 'profesor_id', 'organizacion', 'periodo', 'nivel_experiencia', 'descripcion']
        read_only_fields = ['diseno_id']

class LogroProfesionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogroProfesional
        fields = ['logro_id', 'profesor_id', 'descripcion', 'anio', 'relevancia']
        read_only_fields = ['logro_id']

class PremioDistincionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PremioDistincion
        fields = ['premio_id', 'profesor_id', 'descripcion', 'anio', 'institucion_otorga']
        read_only_fields = ['premio_id']

class ParticipacionOrganizacionesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParticipacionOrganizaciones
        fields = ['participacion_id', 'profesor_id', 'nombre_organizacion', 'periodo', 'nivel_participacion']
        read_only_fields = ['participacion_id']

class CapacitacionDocenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CapacitacionDocente
        fields = ['capacitacion_id', 'profesor_id', 'nombre_curso', 'institucion', 'pais', 'anio_obtencion', 'horas']
        read_only_fields = ['capacitacion_id']

class ActualizacionDisciplinarSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActualizacionDisciplinar
        fields = ['actualizacion_id', 'profesor_id', 'nombre_curso', 'institucion', 'pais', 'anio_obtencion', 'horas']
        read_only_fields = ['actualizacion_id']

class ProductoAcademicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductoAcademico
        fields = ['producto_id', 'profesor_id', 'descripcion', 'anio', 'tipo', 'detalles']
        read_only_fields = ['producto_id']
