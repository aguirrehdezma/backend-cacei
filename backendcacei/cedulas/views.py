from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from usuarios_y_acceso.permissions import IsCoordinadorOrAdmin, ReadOnly
from cedulas.serializers import CedulaAEPVsAECACEISerializer, CedulaAEPVsOESerializer, CedulaCursosVsAEPSerializer, CedulaCvSinteticoSerializer, CedulaHerramientasValoracionAEPSerializer, CedulaOrganizacionCurricularSerializer, CedulaPlanMejoraSerializer, CedulaProgramaAsignaturaSerializer, CedulaValoracionObjetivosSerializer
from cedulas.models import Cedula

class CedulaViewSet(viewsets.ModelViewSet):
    queryset = Cedula.objects.all()
    # Admin/Coordinador pueden crear/editar, todos pueden leer
    permission_classes = [IsAuthenticated, IsCoordinadorOrAdmin | ReadOnly]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        tipo = self.request.query_params.get("tipo")
        if tipo:
            queryset = queryset.filter(tipo=tipo)
        return queryset
    
    def get_serializer_class(self):
        # Si es retrieve/update
        if self.action in ["retrieve", "update", "partial_update"]:
            cedula = self.get_object()
            if cedula.tipo == Cedula.CV_SINTETICO:
                return CedulaCvSinteticoSerializer
            elif cedula.tipo == Cedula.PLAN_MEJORA:
                return CedulaPlanMejoraSerializer
            elif cedula.tipo == Cedula.VALORACION_OBJETIVOS:
                return CedulaValoracionObjetivosSerializer
            elif cedula.tipo == Cedula.AEP_VS_AECACEI:
                return CedulaAEPVsAECACEISerializer
            elif cedula.tipo == Cedula.AEP_VS_OE:
                return CedulaAEPVsOESerializer
            elif cedula.tipo == Cedula.CURSOS_VS_AEP:
                return CedulaCursosVsAEPSerializer
            elif cedula.tipo == Cedula.HERRAMIENTAS_VALORACION_AEP:
                return CedulaHerramientasValoracionAEPSerializer
            elif cedula.tipo == Cedula.PROGRAMA_ASIGNATURA:
                return CedulaProgramaAsignaturaSerializer
            return CedulaOrganizacionCurricularSerializer
        
        # Para create/list, usa el tipo desde request
        tipo = self.request.data.get("tipo") or self.request.query_params.get("tipo")
        if tipo == Cedula.CV_SINTETICO:
            return CedulaCvSinteticoSerializer
        elif tipo == Cedula.PLAN_MEJORA:
            return CedulaPlanMejoraSerializer
        elif tipo == Cedula.VALORACION_OBJETIVOS:
            return CedulaValoracionObjetivosSerializer
        elif tipo == Cedula.AEP_VS_AECACEI:
            return CedulaAEPVsAECACEISerializer
        elif tipo == Cedula.AEP_VS_OE:
            return CedulaAEPVsOESerializer
        elif tipo == Cedula.CURSOS_VS_AEP:
            return CedulaCursosVsAEPSerializer
        elif tipo == Cedula.HERRAMIENTAS_VALORACION_AEP:
            return CedulaHerramientasValoracionAEPSerializer
        elif tipo == Cedula.PROGRAMA_ASIGNATURA:
            return CedulaProgramaAsignaturaSerializer
        return CedulaOrganizacionCurricularSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        cedula_tipo = self.request.data.get("tipo") or self.request.query_params.get("tipo")
        # Incluir el curso en la serialización de EvaluacionIndicadorCedula
        context["include_curso"] = cedula_tipo == Cedula.HERRAMIENTAS_VALORACION_AEP
        return context
