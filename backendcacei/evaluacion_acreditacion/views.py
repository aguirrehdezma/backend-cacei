from rest_framework import viewsets

from evaluacion_acreditacion.models import AccionMejora, Indicador, EvaluacionIndicador, AportacionPE, GestionAcademica, Hallazgo, Auditoria
from evaluacion_acreditacion.serializers import AccionMejoraSerializer, IndicadorSerializer, EvaluacionIndicadorSerializer, AportacionPESerializer, GestionAcademicaSerializer, HallazgoSerializer, AuditoriaSerializer

# Create your views here.
class AccionMejoraViewSet(viewsets.ModelViewSet):
    queryset = AccionMejora.objects.all()
    serializer_class = AccionMejoraSerializer

class IndicadorViewSet(viewsets.ModelViewSet):
    queryset = Indicador.objects.all()
    serializer_class = IndicadorSerializer

class EvaluacionIndicadorViewSet(viewsets.ModelViewSet):
    queryset = EvaluacionIndicador.objects.all()
    serializer_class = EvaluacionIndicadorSerializer

class AportacionPEViewSet(viewsets.ModelViewSet):
    queryset = AportacionPE.objects.all()
    serializer_class = AportacionPESerializer

class GestionAcademicaViewSet(viewsets.ModelViewSet):
    queryset = GestionAcademica.objects.all()
    serializer_class = GestionAcademicaSerializer

class HallazgoViewSet(viewsets.ModelViewSet):
    queryset = Hallazgo.objects.all()
    serializer_class = HallazgoSerializer

class AuditoriaViewSet(viewsets.ModelViewSet):
    queryset = Auditoria.objects.all()
    serializer_class = AuditoriaSerializer
