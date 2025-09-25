from rest_framework import serializers
from gestion_de_profesores.models import Profesores
from gestion_de_profesores.models import ProfesoresCursos
from gestion_de_profesores.models import FormacionAcademica
from gestion_de_profesores.models import ExperienciaProfesional
from gestion_de_profesores.models import ExperienciaDiseno
from gestion_de_profesores.models import LogrosProfesionales
from gestion_de_profesores.models import PremiosDistinciones
from gestion_de_profesores.models import ParticipacionOrganizaciones
from gestion_de_profesores.models import CapacitacionDocente
from gestion_de_profesores.models import ActualizacionDisciplinar
from gestion_de_profesores.models import ProductoAcademico

# Create your serializers here.

class ProfesoresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profesores
        fields = [
            'profesor_id',
            'numero_empleado',
            'apellido_paterno',
            'apellido_materno',
            'nombres',
            'fecha_nacimiento',
            'nombramiento_actual',
            'antiguedad',
            'experiencia_ingenieria',
            'created_at',
            'updated_at'
        ]


class ProfesoresCursosSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfesoresCursos
        fields = [
            'profesor_curso_id',
            'profesor_id',
            'curso_id',
            'tipo',
            'periodo',
            'created_at',
            'updated_at'
        ]


class FormacionAcademicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormacionAcademica
        fields = [
            'formacion_id',
            'profesor_id',
            'nivel',
            'institucion',
            'pais',
            'anno_obtencion',
            'cedula_profesional',
            'especialidad',
            'created_at',
            'updated_at'
        ]
        

class ExperienciaProfesionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExperienciaProfesional
        fields = [
            'experiencia_id',
            'profesor_id',
            'organización',
            'puesto',
            'fecha_inicio',
            'fecha_fin',
            'actividades',
            'created_at',
            'updated_at'
        ]
        
class ExperienciaDisenoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExperienciaDiseno
        fields = [
            'diseno_id',
            'profesor_id',
            'organizacion',
            'periodo',
            'nivel_experiencia',
            'descripcion',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['diseno_id']
        
class LogrosProfesionalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogrosProfesionales
        fields = [
            'logro_id',
            'profesor_id',
            'descripcion',
            'anno',
            'relevancia',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['logro_id']
        

class PremiosDistincionesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PremiosDistinciones
        fields = [
            'premio_id',
            'profesor_id',
            'descripcion',
            'anno',
            'institucion_otorga',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['premio_id']
 

class ParticipacionOrganizacionesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParticipacionOrganizaciones
        fields = [
            'participacion_id',
            'profesor_id',
            'organizacion',
            'periodo',
            'nivel_participacion',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['participacion_id']


class CapacitacionDocenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CapacitacionDocente
        fields = [
            'capacitacion_id',
            'profesor_id',
            'nombre_curso',
            'institucion',
            'pais',
            'anno_obtencion',
            'horas',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['capacitacion_id']


class ActualizacionDisciplinarSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActualizacionDisciplinar
        fields = [
            'actualizacion_id',
            'profesor_id',
            'nombre_curso',
            'institucion',
            'pais',
            'anno_obtencion',
            'horas',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['actualizacion_id']

class ProductoAcademicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductoAcademico
        fields = [
            'producto_id', 
            'descripcion',
            'anno',
            'tipo',
            'detalles'
            ]
        read_only_fields = ['producto_id']