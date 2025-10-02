from rest_framework import viewsets

from core.models import Curso, Profesor, ProgramaEducativo
from core.serializers import CursoSerializer, ProfesorSerializer, ProgramaEducativoSerializer

# Create your views here.
class ProfesorViewSet(viewsets.ModelViewSet):
    queryset = Profesor.objects.all()
    serializer_class = ProfesorSerializer

class ProgramaEducativoViewSet(viewsets.ModelViewSet):
    queryset = ProgramaEducativo.objects.all()
    serializer_class = ProgramaEducativoSerializer

class CursoViewSet(viewsets.ModelViewSet):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer
