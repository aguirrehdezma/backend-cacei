from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from usuarios_y_acceso.permissions import IsCoordinadorOrAdmin, IsDocenteOwner
from evaluacion_acreditacion.models import AccionMejora, Indicador, EvaluacionIndicador, AportacionPE, GestionAcademica, Hallazgo, Auditoria
from evaluacion_acreditacion.serializers import AccionMejoraSerializer, IndicadorSerializer, EvaluacionIndicadorSerializer, AportacionPESerializer, GestionAcademicaSerializer, HallazgoSerializer, AuditoriaSerializer

# Create your views here.
class AccionMejoraViewSet(viewsets.ModelViewSet):
    queryset = AccionMejora.objects.all()
    serializer_class = AccionMejoraSerializer
    permission_classes = [IsAuthenticated, IsCoordinadorOrAdmin]

class IndicadorViewSet(viewsets.ModelViewSet):
    queryset = Indicador.objects.all()
    serializer_class = IndicadorSerializer
    permission_classes = [IsAuthenticated, IsCoordinadorOrAdmin]

class EvaluacionIndicadorViewSet(viewsets.ModelViewSet):
    queryset = EvaluacionIndicador.objects.all()
    serializer_class = EvaluacionIndicadorSerializer
    permission_classes = [IsAuthenticated, IsCoordinadorOrAdmin]

class AportacionPEViewSet(viewsets.ModelViewSet):
    queryset = AportacionPE.objects.all()
    serializer_class = AportacionPESerializer
    permission_classes = [IsAuthenticated, IsDocenteOwner]
    
    def get_queryset(self):
        user = self.request.user
        if user.role in ['admin', 'coordinador']:
            return AportacionPE.objects.all()
        elif user.role == 'docente' and hasattr(user, 'profesor_profile'):
            return AportacionPE.objects.filter(profesor=user.profesor_profile)
        return AportacionPE.objects.none()
    
    def perform_create(self, serializer):
        if self.request.user.role == 'docente' and hasattr(self.request.user, 'profesor_profile'):
            serializer.save(profesor=self.request.user.profesor_profile)
        else:
            serializer.save()

class GestionAcademicaViewSet(viewsets.ModelViewSet):
    queryset = GestionAcademica.objects.all()
    serializer_class = GestionAcademicaSerializer
    permission_classes = [IsAuthenticated, IsDocenteOwner]
    
    def get_queryset(self):
        user = self.request.user
        if user.role in ['admin', 'coordinador']:
            return GestionAcademica.objects.all()
        elif user.role == 'docente' and hasattr(user, 'profesor_profile'):
            return GestionAcademica.objects.filter(profesor=user.profesor_profile)
        return GestionAcademica.objects.none()
    
    def perform_create(self, serializer):
        if self.request.user.role == 'docente' and hasattr(self.request.user, 'profesor_profile'):
            serializer.save(profesor=self.request.user.profesor_profile)
        else:
            serializer.save()

class HallazgoViewSet(viewsets.ModelViewSet):
    queryset = Hallazgo.objects.all()
    serializer_class = HallazgoSerializer
    permission_classes = [IsAuthenticated, IsCoordinadorOrAdmin]

class AuditoriaViewSet(viewsets.ModelViewSet):
    queryset = Auditoria.objects.all()
    serializer_class = AuditoriaSerializer
    permission_classes = [IsAuthenticated, IsCoordinadorOrAdmin]
