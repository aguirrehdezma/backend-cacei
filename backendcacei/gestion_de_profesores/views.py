from rest_framework import viewsets

from gestion_de_profesores.models import ActualizacionDisciplinar, CapacitacionDocente, ExperienciaDiseno, ExperienciaProfesional, FormacionAcademica, LogroProfesional, ParticipacionOrganizaciones, PremioDistincion, Profesor, ProfesorCurso
from gestion_de_profesores.serializers import ActualizacionDisciplinarSerializer, CapacitacionDocenteSerializer, ExperienciaDisenoSerializer, ExperienciaProfesionalSerializer, FormacionAcademicaSerializer, LogroProfesionalSerializer, ParticipacionOrganizacionesSerializer, PremioDistincionSerializer, ProfesorCursoSerializer, ProfesorSerializer

# Create your views here.
class ProfesorViewSet(viewsets.ModelViewSet):
    queryset = Profesor.objects.all()
    serializer_class = ProfesorSerializer

class ProfesorCursoViewSet(viewsets.ModelViewSet):
    queryset = ProfesorCurso.objects.all()
    serializer_class = ProfesorCursoSerializer

class FormacionAcademicaViewSet(viewsets.ModelViewSet):
    queryset = FormacionAcademica.objects.all()
    serializer_class = FormacionAcademicaSerializer

class ExperienciaProfesionalViewSet(viewsets.ModelViewSet):
    queryset = ExperienciaProfesional.objects.all()
    serializer_class = ExperienciaProfesionalSerializer

class ExperienciaDisenoViewSet(viewsets.ModelViewSet):
    queryset = ExperienciaDiseno.objects.all()
    serializer_class = ExperienciaDisenoSerializer

class LogroProfesionalViewSet(viewsets.ModelViewSet):
    queryset = LogroProfesional.objects.all()
    serializer_class = LogroProfesionalSerializer

class PremioDistincionViewSet(viewsets.ModelViewSet):
    queryset = PremioDistincion.objects.all()
    serializer_class = PremioDistincionSerializer

class ParticipacionOrganizacionesViewSet(viewsets.ModelViewSet):
    queryset = ParticipacionOrganizaciones.objects.all()
    serializer_class = ParticipacionOrganizacionesSerializer

class CapacitacionDocenteViewSet(viewsets.ModelViewSet):
    queryset = CapacitacionDocente.objects.all()
    serializer_class = CapacitacionDocenteSerializer

class ActualizacionDisciplinarViewSet(viewsets.ModelViewSet):
    queryset = ActualizacionDisciplinar.objects.all()
    serializer_class = ActualizacionDisciplinarSerializer
