from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from core.models import Curso, Institucion, Organizacion, Periodo, Profesor, ProgramaEducativo
from core.serializers import CursoSerializer, InstitucionSerializer, OrganizacionSerializer, PeriodoSerializer, ProfesorSerializer, ProgramaEducativoSerializer
from usuarios_y_acceso.permissions import IsAdmin, IsCoordinadorOrAdmin, ReadOnly

# Create your views here.
class ProfesorViewSet(viewsets.ModelViewSet):
    queryset = Profesor.objects.all()
    serializer_class = ProfesorSerializer
    
    # Admin y Coordinador pueden crear/editar, Docentes solo leen
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        else:  # create, update, partial_update, destroy
            permission_classes = [IsAuthenticated, IsCoordinadorOrAdmin]
        return [permission() for permission in permission_classes]

class ProgramaEducativoViewSet(viewsets.ModelViewSet):
    queryset = ProgramaEducativo.objects.all()
    serializer_class = ProgramaEducativoSerializer
    # Solo Admin/Coordinador
    permission_classes = [IsAuthenticated, IsCoordinadorOrAdmin]
    
class CursoViewSet(viewsets.ModelViewSet):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer
    # Todos pueden ver, solo Admin/Coordinador modifican
    permission_classes = [IsAuthenticated, IsCoordinadorOrAdmin | ReadOnly]

class InstitucionViewSet(viewsets.ModelViewSet):
    queryset = Institucion.objects.all()
    serializer_class = InstitucionSerializer
    permission_classes = [IsAuthenticated]

class OrganizacionViewSet(viewsets.ModelViewSet):
    queryset = Organizacion.objects.all()
    serializer_class = OrganizacionSerializer
    permission_classes = [IsAuthenticated]

class PeriodoViewSet(viewsets.ModelViewSet):
    queryset = Periodo.objects.all()
    serializer_class = PeriodoSerializer
    # Todos pueden ver, solo Admin modifica
    permission_classes = [IsAuthenticated, IsAdmin | ReadOnly]
