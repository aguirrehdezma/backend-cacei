from rest_framework import viewsets

from gestion_academica.models import Bibliografia, CriterioDesempeno, Curso, EjeConocimiento, EstrategiaEnsenanza, EstrategiaEvaluacion, HorasSemana, ObjetivoEducacional, ProductoAcademico, ProgramaEducativo, UnidadTematica
from gestion_academica.serializers import BibliografiaSerializer, CriterioDesempenoSerializer, CursoSerializer, EjeConocimientoSerializer, EstrategiaEnsenanzaSerializer, EstrategiaEvaluacionSerializer, HorasSemanaSerializer, ObjetivoEducacionalSerializer, ProductoAcademicoSerializer, ProgramaEducativoSerializer, UnidadTematicaSerializer

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

class BibliografiaViewSet(viewsets.ModelViewSet):
    queryset = Bibliografia.objects.all()
    serializer_class = BibliografiaSerializer

class HorasSemanaViewSet(viewsets.ModelViewSet):
    queryset = HorasSemana.objects.all()
    serializer_class = HorasSemanaSerializer

class ProductoAcademicoViewSet(viewsets.ModelViewSet):
    queryset = ProductoAcademico.objects.all()
    serializer_class = ProductoAcademicoSerializer

class EjeConocimientoViewSet(viewsets.ModelViewSet):
    queryset = EjeConocimiento.objects.all()
    serializer_class = EjeConocimientoSerializer
