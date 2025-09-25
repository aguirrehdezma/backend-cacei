from django.shortcuts import render
from rest_framework import viewsets
from .models import AccionMejora
from .serializers import AccionMejoraSerializer
from .models import Indicador
from .serializers import IndicadorSerializer
from .models import Evaluacion_Indicador
from .serializers import EvaluacionIndicadorSerializer
from .models import aportacion_pe
from .serializers import AportacionPESerializer
from .models import Gestion_Academica
from .serializers import GestionAcademicaSerializer
from .models import Hallazgo
from .serializers import HallazgoSerializer
from .models import Auditoria
from .serializers import AuditoriaSerializer





# Create your views here.
class AccionMejoraViewSet(viewsets.ModelViewSet):
    queryset = AccionMejora.objects.all()
    serializer_class = AccionMejoraSerializer

class IndicadorViewSet(viewsets.ModelViewSet):
    queryset = Indicador.objects.all()
    serializer_class = IndicadorSerializer

class EvaluacionIndicadorViewSet(viewsets.ModelViewSet):
    queryset = Evaluacion_Indicador.objects.all()
    serializer_class = EvaluacionIndicadorSerializer

class AportacionPEViewSet(viewsets.ModelViewSet):
    queryset = aportacion_pe.objects.all()
    serializer_class = AportacionPESerializer


class GestionAcademicaViewSet(viewsets.ModelViewSet):
    queryset = Gestion_Academica.objects.all()
    serializer_class = GestionAcademicaSerializer


class HallazgoViewSet(viewsets.ModelViewSet):
    queryset = Hallazgo.objects.all()
    serializer_class = HallazgoSerializer


class AuditoriaViewSet(viewsets.ModelViewSet):
    queryset = Auditoria.objects.all()
    serializer_class = AuditoriaSerializer