from rest_framework import viewsets

from gestion_academica.models import CriterioDesempeno, Curso, EstrategiaEnsenanza, EstrategiaEvaluacion, ObjetivoEducacional, ProgramaEducativo, UnidadTematica
from gestion_academica.serializers import CriterioDesempenoSerializer, CursoSerializer, EstrategiaEnsenanzaSerializer, EstrategiaEvaluacionSerializer, ObjetivoEducacionalSerializer, ProgramaEducativoSerializer, UnidadTematicaSerializer

# Create your views here.
class ProgramaEducativoViewSet(viewsets.ModelViewSet):
    queryset = ProgramaEducativo.objects.all()
    serializer_class = ProgramaEducativoSerializer
    
class UnidadTematicaViewSet(viewsets.ModelViewSet):
    queryset = UnidadTematica.objects.all()
    serializer_class = UnidadTematicaSerializer
    
class CriterioDesempenoViewSet(viewsets.ModelViewSet):
    queryset = CriterioDesempeno.objects.all()
    serializer_class = CriterioDesempenoSerializer

class CursoViewSet(viewsets.ModelViewSet):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer

class EstrategiaEnsenanzaViewSet(viewsets.ModelViewSet):
    queryset = EstrategiaEnsenanza.objects.all()
    serializer_class = EstrategiaEnsenanzaSerializer

class EstrategiaEvaluacionViewSet(viewsets.ModelViewSet):
    queryset = EstrategiaEvaluacion.objects.all()
    serializer_class = EstrategiaEvaluacionSerializer

class ObjetivoEducacionalViewSet(viewsets.ModelViewSet):
    queryset = ObjetivoEducacional.objects.all()
    serializer_class = ObjetivoEducacionalSerializer
