from rest_framework import viewsets

from gestion_academica.models import CriterioDesempeno, ProgramaEducativo, UnidadTematica
from gestion_academica.serializers import CriterioDesempenoSerializer, ProgramaEducativoSerializer, UnidadTematicaSerializer

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
