from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from gestion_de_profesores.models import Profesores
from gestion_de_profesores.models import ProfesoresCursos
from gestion_de_profesores.models import FormacionAcademica
from gestion_de_profesores.models import ExperienciaProfesional
from gestion_de_profesores.models import ExperienciaDiseno
from gestion_de_profesores.models import LogrosProfesionales
from gestion_de_profesores.models import PremiosDistinciones
from gestion_de_profesores.models import ParticipacionOrganizaciones
from gestion_de_profesores.models import CapacitacionDocente
from gestion_de_profesores.models import ActualizacionDisciplinar
from gestion_de_profesores.models import ProductoAcademico
from gestion_de_profesores.serializers import ProfesoresSerializer
from gestion_de_profesores.serializers import ProfesoresCursosSerializer
from gestion_de_profesores.serializers import FormacionAcademicaSerializer
from gestion_de_profesores.serializers import ExperienciaProfesionalSerializer
from gestion_de_profesores.serializers import ExperienciaDisenoSerializer
from gestion_de_profesores.serializers import LogrosProfesionalesSerializer
from gestion_de_profesores.serializers import PremiosDistincionesSerializer
from gestion_de_profesores.serializers import ParticipacionOrganizacionesSerializer
from gestion_de_profesores.serializers import CapacitacionDocenteSerializer
from gestion_de_profesores.serializers import ActualizacionDisciplinarSerializer
from gestion_de_profesores.models import ActualizacionDisciplinar
from gestion_de_profesores.serializers import ProductoAcademicoSerializer

# Create your views here.

class ProfesoresView(APIView):
    queryset = Profesores.objects.all()
    serializerClas = ProfesoresSerializer
    

class ProfesoresCursosView(APIView):
    queryset = ProfesoresCursos.objects.all()
    serializerClas = ProfesoresCursosSerializer
    

class FormacionAcademicaView(APIView):
    queryset = FormacionAcademica.objects.all()
    serializerClas = FormacionAcademicaSerializer


class ExperienciaProfesionalView(APIView):
    queryset = ExperienciaProfesional.objects.all()
    serializerClas = ExperienciaProfesionalSerializer
    

class ExperienciaDisenoView(APIView):
    queryset = ExperienciaDiseno.objects.all()
    serializerClas = ExperienciaDisenoSerializer
    
    
class LogrosProfesionalesView(APIView):
    queryset = LogrosProfesionales.objects.all()
    serializerClas = LogrosProfesionalesSerializer
    
    
class PremiosDistincionesView(APIView):
    queryset = PremiosDistinciones.objects.all()
    serializerClas = PremiosDistincionesSerializer
    
     
class ParticipacionOrganizacionesView(APIView):
    queryset = ParticipacionOrganizaciones.objects.all()
    serializerClas = ParticipacionOrganizacionesSerializer
    
     
class CapacitacionDocenteView(APIView):
    queryset = CapacitacionDocente.objects.all()
    serializerClas = CapacitacionDocenteSerializer
    
    
class ActualizacionDisciplinarView(APIView):
    queryset = ActualizacionDisciplinar.objects.all()
    serializerClas = ActualizacionDisciplinarSerializer
    
    
class ProductoAcademicoView(APIView):
    queryset = ProductoAcademico.objects.all()
    serializerClas = ProductoAcademicoSerializer
    
    
# Create your views here.
