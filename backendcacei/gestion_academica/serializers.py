from rest_framework import serializers

from evaluacion_acreditacion.serializers import IndicadorSerializer
from gestion_academica.models import AtributoCACEI, AtributoPE, AtributoPECACEI, AtributoPEObjetivo, Bibliografia, CriterioDesempeno, CursoAtributoPE, CursoEje, EjeConocimiento, EstrategiaEnsenanza, EstrategiaEvaluacion, HorasSemana, ObjetivoEducacional, ObjetivoEspecifico, Practica, UnidadTematica

class UnidadTematicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnidadTematica
        fields = ['unidad_id', 'curso_id', 'numero', 'descripcion']
        read_only_fields = ['unidad_id']

class CriterioDesempenoSerializer(serializers.ModelSerializer):
    indicadores = IndicadorSerializer(many=True, read_only=True)
    
    class Meta:
        model = CriterioDesempeno
        fields = ['criterio_id', 'atributo_pe_id', 'codigo', 'descripcion', 'indicadores']
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

class AtributoCACEISerializer(serializers.ModelSerializer):
    class Meta:
        model = AtributoCACEI
        fields = ['atributo_cacei_id', 'codigo', 'nombre', 'descripcion', 'wk_referencia']
        read_only_fields = ['atributo_cacei_id']

class AtributoPECACEISerializer(serializers.ModelSerializer):
    atributo_cacei = AtributoCACEISerializer(read_only=True, source='atributo_cacei_id')

    class Meta:
        model = AtributoPECACEI
        fields = ['atributo_pe_cacei_id', 'atributo_pe_id', 'atributo_cacei_id', 'justificacion', 'atributo_cacei']
        read_only_fields = ['atributo_pe_cacei_id']

class AtributoPEObjetivoSerializer(serializers.ModelSerializer):
    valoracion_aep = serializers.SerializerMethodField()
    objetivos_educacionales = ObjetivoEducacionalSerializer(read_only=True, source='objetivo_id')

    class Meta:
        model = AtributoPEObjetivo
        fields = ['atributo_pe_objetivo_id', 'atributo_pe_id', 'objetivo_id', 'justificacion', 'valoracion_aep', 'objetivos_educacionales']
        read_only_fields = ['atributo_pe_objetivo_id']
    
    def get_valoracion_aep(self, obj):
        from cedulas.serializers import CedulaHerramientasValoracionAEPSerializer  
        return CedulaHerramientasValoracionAEPSerializer(obj.atributo_pe_id).data

class AtributoPESerializer(serializers.ModelSerializer):
    atributo_pe_cacei = AtributoPECACEISerializer(many=True, read_only=True)
    atributo_pe_objetivo = AtributoPEObjetivoSerializer(many=True, read_only=True)

    class Meta:
        model = AtributoPE
        fields = ['atributo_pe_id', 'programa_id', 'codigo', 'nombre', 'nombre_abreviado', 'descripcion', 'atributo_pe_cacei', 'atributo_pe_objetivo']
        read_only_fields = ['atributo_pe_id']

class CursoAtributoPESerializer(serializers.ModelSerializer):
    atributo_pe = AtributoPESerializer(read_only=True, source='atributo_pe_id')

    class Meta:
        model = CursoAtributoPE
        fields = ['curso_atributo_pe_id', 'curso_id', 'atributo_pe_id', 'nivel_aporte', 'atributo_pe']
        read_only_fields = ['curso_atributo_pe_id']

class CursoEjeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CursoEje
        fields = ['curso_eje_id', 'curso_id', 'eje_id', 'horas']
        read_only_fields = ['curso_eje_id']

class PracticaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Practica
        fields = ['practica_id', 'curso_id', 'numero', 'descripcion']
        read_only_fields = ['practica_id']
