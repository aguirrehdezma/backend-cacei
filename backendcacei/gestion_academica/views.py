from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from usuarios_y_acceso.permissions import IsCoordinadorOrAdmin, ReadOnly
from gestion_academica.models import Actividad, Alumno, AtributoCACEI, AtributoPE, AtributoPECACEI, AtributoPEObjetivo, Bibliografia, Calificacion, CriterioDesempeno, CursoAtributoPE, CursoEje, EjeConocimiento, EstrategiaEnsenanza, EstrategiaEvaluacion, HorasSemana, ObjetivoEducacional, ObjetivoEspecifico, Practica, UnidadTematica
from gestion_academica.serializers import ActividadSerializer, AlumnoSerializer, AtributoCACEISerializer, AtributoPECACEISerializer, AtributoPEObjetivoSerializer, AtributoPESerializer, BibliografiaSerializer, CalificacionSerializer, CriterioDesempenoSerializer, CursoAtributoPESerializer, CursoEjeSerializer, EjeConocimientoSerializer, EstrategiaEnsenanzaSerializer, EstrategiaEvaluacionSerializer, HorasSemanaSerializer, ObjetivoEducacionalSerializer, ObjetivoEspecificoSerializer, PracticaSerializer, UnidadTematicaSerializer

# Create your views here.
class UnidadTematicaViewSet(viewsets.ModelViewSet):
    queryset = UnidadTematica.objects.all()
    serializer_class = UnidadTematicaSerializer
    # Solo Admin/Coordinador modifican, todos leen
    permission_classes = [IsAuthenticated, IsCoordinadorOrAdmin | ReadOnly]

class CriterioDesempenoViewSet(viewsets.ModelViewSet):
    queryset = CriterioDesempeno.objects.all()
    serializer_class = CriterioDesempenoSerializer
    # Solo Admin/Coordinador modifican, todos leen
    permission_classes = [IsAuthenticated, IsCoordinadorOrAdmin | ReadOnly]

class EstrategiaEnsenanzaViewSet(viewsets.ModelViewSet):
    queryset = EstrategiaEnsenanza.objects.all()
    serializer_class = EstrategiaEnsenanzaSerializer
    # Solo Admin/Coordinador modifican, todos leen
    permission_classes = [IsAuthenticated, IsCoordinadorOrAdmin | ReadOnly]

class EstrategiaEvaluacionViewSet(viewsets.ModelViewSet):
    queryset = EstrategiaEvaluacion.objects.all()
    serializer_class = EstrategiaEvaluacionSerializer
    # Solo Admin/Coordinador modifican, todos leen
    permission_classes = [IsAuthenticated, IsCoordinadorOrAdmin | ReadOnly]

class ObjetivoEducacionalViewSet(viewsets.ModelViewSet):
    queryset = ObjetivoEducacional.objects.all()
    serializer_class = ObjetivoEducacionalSerializer
    # Solo Admin/Coordinador modifican, todos leen
    permission_classes = [IsAuthenticated, IsCoordinadorOrAdmin | ReadOnly]

class BibliografiaViewSet(viewsets.ModelViewSet):
    queryset = Bibliografia.objects.all()
    serializer_class = BibliografiaSerializer
    permission_classes = [IsAuthenticated]

class HorasSemanaViewSet(viewsets.ModelViewSet):
    queryset = HorasSemana.objects.all()
    serializer_class = HorasSemanaSerializer
    # Solo Admin/Coordinador modifican, todos leen
    permission_classes = [IsAuthenticated, IsCoordinadorOrAdmin | ReadOnly]

class EjeConocimientoViewSet(viewsets.ModelViewSet):
    queryset = EjeConocimiento.objects.all()
    serializer_class = EjeConocimientoSerializer
    # Solo Admin/Coordinador modifican, todos leen
    permission_classes = [IsAuthenticated, IsCoordinadorOrAdmin | ReadOnly]

class ObjetivoEspecificoViewSet(viewsets.ModelViewSet):
    queryset = ObjetivoEspecifico.objects.all()
    serializer_class = ObjetivoEspecificoSerializer
    # Solo Admin/Coordinador modifican, todos leen
    permission_classes = [IsAuthenticated, IsCoordinadorOrAdmin | ReadOnly]

class AtributoPEViewSet(viewsets.ModelViewSet):
    queryset = AtributoPE.objects.all()
    serializer_class = AtributoPESerializer
    # Solo Admin/Coordinador modifican, todos leen
    permission_classes = [IsAuthenticated, IsCoordinadorOrAdmin | ReadOnly]

class AtributoCACEIViewSet(viewsets.ModelViewSet):
    queryset = AtributoCACEI.objects.all()
    serializer_class = AtributoCACEISerializer
    # Solo Admin/Coordinador modifican, todos leen
    permission_classes = [IsAuthenticated, IsCoordinadorOrAdmin | ReadOnly]

class CursoAtributoPEViewSet(viewsets.ModelViewSet):
    queryset = CursoAtributoPE.objects.all()
    serializer_class = CursoAtributoPESerializer
    # Solo Admin/Coordinador modifican, todos leen
    permission_classes = [IsAuthenticated, IsCoordinadorOrAdmin | ReadOnly]

class CursoEjeViewSet(viewsets.ModelViewSet):
    queryset = CursoEje.objects.all()
    serializer_class = CursoEjeSerializer
    # Solo Admin/Coordinador modifican, todos leen
    permission_classes = [IsAuthenticated, IsCoordinadorOrAdmin | ReadOnly]

class AtributoPEObjetivoViewSet(viewsets.ModelViewSet):
    queryset = AtributoPEObjetivo.objects.all()
    serializer_class = AtributoPEObjetivoSerializer
    # Solo Admin/Coordinador modifican, todos leen
    permission_classes = [IsAuthenticated, IsCoordinadorOrAdmin | ReadOnly]

class AtributoPECACEIViewSet(viewsets.ModelViewSet):
    queryset = AtributoPECACEI.objects.all()
    serializer_class = AtributoPECACEISerializer
    # Solo Admin/Coordinador modifican, todos leen
    permission_classes = [IsAuthenticated, IsCoordinadorOrAdmin | ReadOnly]

class PracticaViewSet(viewsets.ModelViewSet):
    queryset = Practica.objects.all()
    serializer_class = PracticaSerializer
    permission_classes = [IsAuthenticated]

class AlumnoViewSet(viewsets.ModelViewSet):
    queryset = Alumno.objects.all()
    serializer_class = AlumnoSerializer
    permission_classes = [IsAuthenticated]

class CalificacionViewSet(viewsets.ModelViewSet):
    queryset = Calificacion.objects.all()
    serializer_class = CalificacionSerializer
    permission_classes = [IsAuthenticated]

class ActividadViewSet(viewsets.ModelViewSet):
    queryset = Actividad.objects.all()
    serializer_class = ActividadSerializer
    permission_classes = [IsAuthenticated]