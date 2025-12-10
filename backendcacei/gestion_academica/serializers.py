from rest_framework import serializers

from gestion_academica.models import Actividad, Alumno, AtributoCACEI, AtributoPE, AtributoPECACEI, AtributoPEObjetivo, Bibliografia, Calificacion, CriterioDesempeno, CursoAtributoPE, CursoEje, EjeConocimiento, EstrategiaEnsenanza, EstrategiaEvaluacion, HorasSemana, ObjetivoEducacional, ObjetivoEspecifico, Practica, UnidadTematica

class UnidadTematicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnidadTematica
        fields = ['id', 'curso', 'numero', 'descripcion']
        read_only_fields = ['id']

class CriterioDesempenoSerializer(serializers.ModelSerializer):    
    class Meta:
        model = CriterioDesempeno
        fields = ['id', 'atributo_pe', 'codigo', 'descripcion']
        read_only_fields = ['id']

class EstrategiaEnsenanzaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstrategiaEnsenanza
        fields = ['id', 'curso', 'numero', 'descripcion']
        read_only_fields = ['id']

class EstrategiaEvaluacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstrategiaEvaluacion
        fields = ['id', 'curso', 'numero', 'descripcion']
        read_only_fields = ['id']

class ObjetivoEducacionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObjetivoEducacional
        fields = ['id', 'programa', 'codigo', 'descripcion']
        read_only_fields = ['id']

class BibliografiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bibliografia
        fields = ['id', 'curso', 'numero', 'autor', 'titulo', 'editorial', 'anio_publicacion']
        read_only_fields = ['id']

class HorasSemanaSerializer(serializers.ModelSerializer):
    class Meta:
        model = HorasSemana
        fields = ['id', 'curso', 'horas_totales', 'horas_aula', 'horas_laboratorio', 'horas_practicas', 'numero_grupos', 'calificacion_promedio', 'porcentaje_aprobacion', 'porcentaje_reprobacion']
        read_only_fields = ['id']

class EjeConocimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EjeConocimiento
        fields = ['id', 'nombre', 'descripcion']
        read_only_fields = ['id']

class ObjetivoEspecificoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObjetivoEspecifico
        fields = ['id', 'curso', 'descripcion', 'orden']
        read_only_fields = ['id']

class AtributoCACEISerializer(serializers.ModelSerializer):
    class Meta:
        model = AtributoCACEI
        fields = ['id', 'codigo', 'nombre', 'descripcion', 'wk_referencia']
        read_only_fields = ['id']

class AtributoPECACEISerializer(serializers.ModelSerializer):
    class Meta:
        model = AtributoPECACEI
        fields = ['id', 'atributo_pe', 'atributo_cacei', 'justificacion']
        read_only_fields = ['id']

class AtributoPEObjetivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AtributoPEObjetivo
        fields = ['id', 'atributo_pe', 'objetivo', 'justificacion']
        read_only_fields = ['id']

class AtributoPESerializer(serializers.ModelSerializer):
    class Meta:
        model = AtributoPE
        fields = ['id', 'programa', 'codigo', 'nombre', 'nombre_abreviado', 'descripcion']
        read_only_fields = ['id']

class CursoAtributoPESerializer(serializers.ModelSerializer):
    class Meta:
        model = CursoAtributoPE
        fields = ['id', 'curso', 'atributo_pe', 'nivel_aporte']
        read_only_fields = ['id']

class CursoEjeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CursoEje
        fields = ['id', 'curso', 'eje', 'horas']
        read_only_fields = ['id']

class PracticaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Practica
        fields = ['id', 'curso', 'numero', 'descripcion']
        read_only_fields = ['id']

class AlumnoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alumno
        fields = ['id', 'matricula', 'nombre', 'apellido1', 'apellido2']
        read_only_fields = ['id']

class CalificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calificacion
        fields = ['id', 'alumno', 'profesor_curso', 'valor']
        read_only_fields = ['id']

class ActividadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actividad
        fields = ['id', 'profesor_curso', 'atributo_pe', 'nombre', 'descripcion']
        read_only_fields = ['id']