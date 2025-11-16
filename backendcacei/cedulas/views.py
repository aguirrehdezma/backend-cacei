from rest_framework import viewsets

from cedulas.serializers import CedulaAEPVsAECACEISerializer, CedulaAEPVsOESerializer, CedulaCursosVsAEPSerializer, CedulaCvSinteticoSerializer, CedulaOrganizacionCurricularSerializer, CedulaPlanMejoraSerializer, CedulaValoracionObjetivosSerializer
from cedulas.models import Cedula

class CedulaViewSet(viewsets.ModelViewSet):
    queryset = Cedula.objects.all()
    
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
        return CedulaOrganizacionCurricularSerializer
