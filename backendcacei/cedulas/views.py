from rest_framework import generics

from gestion_academica.models import AtributoPE
from core.models import Profesor
from evaluacion_acreditacion.models import Hallazgo

from cedulas.serializers import CedulaCVSinteticoSerializer, CedulaHerramientasValoracionAEPSerializer, CedulaPlanMejoraSerializer

# Create your views here.
class CedulaCVSinteticoView(generics.RetrieveAPIView):
    queryset = Profesor.objects.all()
    serializer_class = CedulaCVSinteticoSerializer

class CedulaPlanMejoraView(generics.RetrieveAPIView):
    queryset = Hallazgo.objects.all()
    serializer_class = CedulaPlanMejoraSerializer

class CedulaHerramientasValoracionAEPView(generics.RetrieveAPIView):
    queryset = AtributoPE.objects.all()
    serializer_class = CedulaHerramientasValoracionAEPSerializer
