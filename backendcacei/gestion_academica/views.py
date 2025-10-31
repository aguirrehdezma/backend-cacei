from rest_framework import viewsets

from gestion_academica.models import Alumno, AtributoCACEI, AtributoPE, AtributoPECACEI, AtributoPEObjetivo, Bibliografia, Calificacion, CriterioDesempeno, CursoAtributoPE, CursoEje, EjeConocimiento, EstrategiaEnsenanza, EstrategiaEvaluacion, HorasSemana, ObjetivoEducacional, ObjetivoEspecifico, Practica, UnidadTematica
from gestion_academica.serializers import AlumnoSerializer, AtributoCACEISerializer, AtributoPECACEISerializer, AtributoPEObjetivoSerializer, AtributoPESerializer, BibliografiaSerializer, CalificacionSerializer, CriterioDesempenoSerializer, CursoAtributoPESerializer, CursoEjeSerializer, EjeConocimientoSerializer, EstrategiaEnsenanzaSerializer, EstrategiaEvaluacionSerializer, HorasSemanaSerializer, ObjetivoEducacionalSerializer, ObjetivoEspecificoSerializer, PracticaSerializer, UnidadTematicaSerializer

# Create your views here.
class UnidadTematicaViewSet(viewsets.ModelViewSet):
    queryset = UnidadTematica.objects.all()
    serializer_class = UnidadTematicaSerializer
    
class CriterioDesempenoViewSet(viewsets.ModelViewSet):
    queryset = CriterioDesempeno.objects.all()
    serializer_class = CriterioDesempenoSerializer

class EstrategiaEnsenanzaViewSet(viewsets.ModelViewSet):
    queryset = EstrategiaEnsenanza.objects.all()
    serializer_class = EstrategiaEnsenanzaSerializer

class EstrategiaEvaluacionViewSet(viewsets.ModelViewSet):
    queryset = EstrategiaEvaluacion.objects.all()
    serializer_class = EstrategiaEvaluacionSerializer

class ObjetivoEducacionalViewSet(viewsets.ModelViewSet):
    queryset = ObjetivoEducacional.objects.all()
    serializer_class = ObjetivoEducacionalSerializer

class BibliografiaViewSet(viewsets.ModelViewSet):
    queryset = Bibliografia.objects.all()
    serializer_class = BibliografiaSerializer

class HorasSemanaViewSet(viewsets.ModelViewSet):
    queryset = HorasSemana.objects.all()
    serializer_class = HorasSemanaSerializer

class EjeConocimientoViewSet(viewsets.ModelViewSet):
    queryset = EjeConocimiento.objects.all()
    serializer_class = EjeConocimientoSerializer

class ObjetivoEspecificoViewSet(viewsets.ModelViewSet):
    queryset = ObjetivoEspecifico.objects.all()
    serializer_class = ObjetivoEspecificoSerializer

class AtributoPEViewSet(viewsets.ModelViewSet):
    queryset = AtributoPE.objects.all()
    serializer_class = AtributoPESerializer

class AtributoCACEIViewSet(viewsets.ModelViewSet):
    queryset = AtributoCACEI.objects.all()
    serializer_class = AtributoCACEISerializer

class CursoAtributoPEViewSet(viewsets.ModelViewSet):
    queryset = CursoAtributoPE.objects.all()
    serializer_class = CursoAtributoPESerializer

class CursoEjeViewSet(viewsets.ModelViewSet):
    queryset = CursoEje.objects.all()
    serializer_class = CursoEjeSerializer

class AtributoPEObjetivoViewSet(viewsets.ModelViewSet):
    queryset = AtributoPEObjetivo.objects.all()
    serializer_class = AtributoPEObjetivoSerializer

class AtributoPECACEIViewSet(viewsets.ModelViewSet):
    queryset = AtributoPECACEI.objects.all()
    serializer_class = AtributoPECACEISerializer

class PracticaViewSet(viewsets.ModelViewSet):
    queryset = Practica.objects.all()
    serializer_class = PracticaSerializer

class AlumnoViewSet(viewsets.ModelViewSet):
    queryset = Alumno.objects.all()
    serializer_class = AlumnoSerializer

class CalificacionViewSet(viewsets.ModelViewSet):
    queryset = Calificacion.objects.all()
    serializer_class = CalificacionSerializer
