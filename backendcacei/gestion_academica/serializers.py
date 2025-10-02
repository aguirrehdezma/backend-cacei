from rest_framework import serializers

from gestion_academica.models import AtributoCACEI, AtributoPE, AtributoPEObjetivo, Bibliografia, CriterioDesempeno, CursoAtributoPE, CursoEje, EjeConocimiento, EstrategiaEnsenanza, EstrategiaEvaluacion, HorasSemana, ObjetivoEducacional, ObjetivoEspecifico, Practica, UnidadTematica

class UnidadTematicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnidadTematica
        fields = ['unidad_id', 'curso_id', 'numero', 'descripcion']
        read_only_fields = ['unidad_id']

class CriterioDesempenoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CriterioDesempeno
        fields = ['criterio_id', 'atributo_pe_id', 'codigo', 'descripcion']
        read_only_fields = ['criterio_id']

class EstrategiaEnsenanzaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstrategiaEnsenanza
        fields = ['estrategia_id', 'curso_id', 'numero', 'descripcion']
        read_only_fields = ['estrategia_id']

class EstrategiaEvaluacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstrategiaEvaluacion
        fields = ['estrategia_id', 'curso_id', 'numero', 'descripcion']
        read_only_fields = ['estrategia_id']

class ObjetivoEducacionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObjetivoEducacional
        fields = ['objetivo_id', 'programa_id', 'codigo', 'descripcion']
        read_only_fields = ['objetivo_id']

class BibliografiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bibliografia
        fields = ['bibliografia_id', 'curso_id', 'numero', 'autor', 'titulo', 'editorial', 'anio_publicacion']
        read_only_fields = ['bibliografia_id']

class HorasSemanaSerializer(serializers.ModelSerializer):
    class Meta:
        model = HorasSemana
        fields = ['horas_id', 'curso_id', 'horas_totales', 'horas_aula', 'horas_laboratorio', 'horas_practicas', 'numero_grupos', 'calificacion_promedio', 'porcentaje_aprobacion', 'porcentaje_reprobacion']
        read_only_fields = ['horas_id']

class EjeConocimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EjeConocimiento
        fields = ['eje_id', 'nombre', 'descripcion']
        read_only_fields = ['eje_id']

class ObjetivoEspecificoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObjetivoEspecifico
        fields = ['objetivo_id', 'curso_id', 'descripcion', 'orden']
        read_only_fields = ['objetivo_id']

class AtributoPESerializer(serializers.ModelSerializer):
    class Meta:
        model = AtributoPE
        fields = ['atributo_pe_id', 'programa_id', 'codigo', 'nombre', 'nombre_abreviado', 'descripcion']
        read_only_fields = ['atributo_pe_id']

class AtributoCACEISerializer(serializers.ModelSerializer):
    class Meta:
        model = AtributoCACEI
        fields = ['atributo_cacei_id', 'codigo', 'nombre', 'descripcion', 'wk_referencia']
        read_only_fields = ['atributo_cacei_id']

class CursoAtributoPESerializer(serializers.ModelSerializer):
    class Meta:
        model = CursoAtributoPE
        fields = ['curso_atributo_pe_id', 'curso_id', 'atributo_pe_id', 'nivel_aporte']
        read_only_fields = ['curso_atributo_pe_id']

class CursoEjeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CursoEje
        fields = ['curso_eje_id', 'curso_id', 'eje_id', 'horas']
        read_only_fields = ['curso_eje_id']

class AtributoPEObjetivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AtributoPEObjetivo
        fields = ['atributo_pe_objetivo_id', 'atributo_pe_id', 'objetivo_id', 'justificacion']
        read_only_fields = ['atributo_pe_objetivo_id']

class AtributoPECACEISerializer(serializers.ModelSerializer):
    class Meta:
        model = AtributoPE
        fields = ['atributo_pe_cacei_id', 'atributo_pe_id', 'atributo_cacei_id', 'justificacion']
        read_only_fields = ['atributo_pe_cacei_id']

class PracticaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Practica
        fields = ['practica_id', 'curso_id', 'numero', 'descripcion']
        read_only_fields = ['practica_id']
