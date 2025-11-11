from rest_framework import viewsets

from core.models import Curso, Institucion, Organizacion, Periodo, Profesor, ProgramaEducativo
from core.serializers import CursoSerializer, InstitucionSerializer, OrganizacionSerializer, PeriodoSerializer, ProfesorSerializer, ProgramaEducativoSerializer

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

class InstitucionViewSet(viewsets.ModelViewSet):
    queryset = Institucion.objects.all()
    serializer_class = InstitucionSerializer

class OrganizacionViewSet(viewsets.ModelViewSet):
    queryset = Organizacion.objects.all()
    serializer_class = OrganizacionSerializer

class PeriodoViewSet(viewsets.ModelViewSet):
    queryset = Periodo.objects.all()
    serializer_class = PeriodoSerializer
