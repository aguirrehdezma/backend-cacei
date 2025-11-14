from rest_framework import viewsets

from cedulas.serializers import  CursoObligatorioSerializer, CursoOptativoSerializer, CedulaCvSinteticoSerializer, CedulaOrganizacionCurricularSerializer
from cedulas.models import Cedula, CursoObligatorio, CursoOptativo

class CursoObligatorioViewSet(viewsets.ModelViewSet):
    queryset = CursoObligatorio.objects.all()
    serializer_class = CursoObligatorioSerializer

class CursoOptativoViewSet(viewsets.ModelViewSet):
    queryset = CursoOptativo.objects.all()
    serializer_class = CursoOptativoSerializer

class CedulaViewSet(viewsets.ModelViewSet):
    queryset = Cedula.objects.all()

    def get_serializer_class(self):
        # Si es retrieve/update
        if self.action in ["retrieve", "update", "partial_update"]:
            cedula = self.get_object()
            if cedula.tipo == Cedula.CV_SINTETICO:
                return CedulaCvSinteticoSerializer
            return CedulaOrganizacionCurricularSerializer

        # Para create/list, usa el tipo desde request
        # /api/cedulas/?tipo=X
        tipo = self.request.data.get("tipo") or self.request.query_params.get("tipo")
        if tipo == Cedula.CV_SINTETICO:
            return CedulaCvSinteticoSerializer
        return CedulaOrganizacionCurricularSerializer
