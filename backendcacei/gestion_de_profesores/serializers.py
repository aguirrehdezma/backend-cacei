from rest_framework import serializers

from gestion_de_profesores.models import ActualizacionDisciplinar, CapacitacionDocente, ExperienciaDiseno, ExperienciaProfesional, FormacionAcademica, LogroProfesional, ParticipacionOrganizaciones, PremioDistincion, ProductoAcademico, ProfesorCurso

class ProfesorCursoSerializer(serializers.ModelSerializer):    
    class Meta:
        model = ProfesorCurso
        fields = ['id', 'profesor', 'curso', 'tipo', 'grupo_seccion', 'periodo']
        read_only_fields = ['id']

class FormacionAcademicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormacionAcademica
        fields = ['id', 'profesor', 'institucion', 'nivel', 'pais', 'anio_obtencion', 'cedula_profesional', 'especialidad']
        read_only_fields = ['id']

class ExperienciaProfesionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExperienciaProfesional
        fields = ['id', 'profesor', 'organizacion', 'puesto', 'fecha_inicio', 'fecha_fin', 'actividades']
        read_only_fields = ['id']

class ExperienciaDisenoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExperienciaDiseno
        fields = ['id', 'profesor', 'organizacion', 'periodo', 'nivel_experiencia', 'descripcion']
        read_only_fields = ['id']

class LogroProfesionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogroProfesional
        fields = ['id', 'profesor', 'descripcion', 'anio', 'relevancia']
        read_only_fields = ['id']

class PremioDistincionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PremioDistincion
        fields = ['id', 'profesor', 'descripcion', 'anio', 'institucion_otorga']
        read_only_fields = ['id']

class ParticipacionOrganizacionesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParticipacionOrganizaciones
        fields = ['id', 'profesor', 'organizacion', 'periodo', 'nivel_participacion']
        read_only_fields = ['id']

class CapacitacionDocenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CapacitacionDocente
        fields = ['id', 'profesor', 'institucion', 'nombre_curso', 'pais', 'anio_obtencion', 'horas']
        read_only_fields = ['id']

class ActualizacionDisciplinarSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActualizacionDisciplinar
        fields = ['id', 'profesor', 'institucion', 'nombre_curso', 'pais', 'anio_obtencion', 'horas']
        read_only_fields = ['id']

class ProductoAcademicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductoAcademico
        fields = ['id', 'profesor', 'descripcion', 'anio', 'tipo', 'detalles']
        read_only_fields = ['id']