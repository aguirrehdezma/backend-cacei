from rest_framework import generics
from rest_framework import viewsets

from cedulas.serializers import  CursoObligatorioSerializer, CursoOptativoSerializer, CedulaCvSinteticoSerializer, CedulaOrganizacionCurricularSerializer
from cedulas.models import Cedula, CursoObligatorio, CursoOptativo
from gestion_academica.models import AtributoPE, ObjetivoEducacional
from core.models import Profesor, Curso, ProgramaEducativo
from evaluacion_acreditacion.models import Hallazgo

# from cedulas.serializers import CedulaAEPVsAECACEISerializer, CedulaAEPVsOESerializer, CedulaCVSinteticoSerializer, CedulaHerramientasValoracionAEPSerializer, CedulaPlanMejoraSerializer, CedulaProgramaAsignaturaSerializer, CedulaSerializer, CedulaValoracionOEPESerializer, CedulaOrganizacionCurricularSerializer, CedulaCursosVsAEPSerializer, CursoObligatorioSerializer, CursoOptativoSerializer

# Create your views here.
'''
class CedulaCVSinteticoView(generics.RetrieveAPIView):
    queryset = Profesor.objects.all()
    serializer_class = CedulaCVSinteticoSerializer

class CedulaPlanMejoraView(generics.RetrieveAPIView):
    queryset = Hallazgo.objects.all()
    serializer_class = CedulaPlanMejoraSerializer

class CedulaHerramientasValoracionAEPView(generics.RetrieveAPIView):
    queryset = AtributoPE.objects.all()
    serializer_class = CedulaHerramientasValoracionAEPSerializer

class CedulaProgramaAsignaturaView(generics.RetrieveAPIView):
    queryset = Curso.objects.all()
    serializer_class = CedulaProgramaAsignaturaSerializer

class CedulaValoracionOEPEView(generics.RetrieveAPIView):
    queryset = ObjetivoEducacional.objects.all()
    serializer_class = CedulaValoracionOEPESerializer

class CedulaOrganizacionCurricularView(generics.RetrieveAPIView):
    queryset = ProgramaEducativo.objects.all()
    serializer_class = CedulaOrganizacionCurricularSerializer

class CedulaCursosVsAEPView(generics.RetrieveAPIView):
    queryset = ProgramaEducativo.objects.all()
    serializer_class = CedulaCursosVsAEPSerializer

class CedulaAEPVsAECACEIView(generics.RetrieveAPIView):
    queryset = ProgramaEducativo.objects.all()
    serializer_class = CedulaAEPVsAECACEISerializer

class CedulaAEPVsOEView(generics.RetrieveAPIView):
    queryset = ProgramaEducativo.objects.all()
    serializer_class = CedulaAEPVsOESerializer
'''



class CursoObligatorioViewSet(viewsets.ModelViewSet):
    queryset = CursoObligatorio.objects.all()
    serializer_class = CursoObligatorioSerializer

class CursoOptativoViewSet(viewsets.ModelViewSet):
    queryset = CursoOptativo.objects.all()
    serializer_class = CursoOptativoSerializer

class CedulaViewSet(viewsets.ModelViewSet):
    queryset = Cedula.objects.all()

    def get_serializer_class(self):
        cedula = self.get_object() if self.action in ['retrieve', 'update'] else None
        tipo = cedula.tipo if cedula else self.request.data.get('tipo')

        if tipo == Cedula.CV_SINTETICO:
            return CedulaCvSinteticoSerializer
        return CedulaOrganizacionCurricularSerializer
        #checar la seleccion del tipo de cedula y regresar el serializer adecuado