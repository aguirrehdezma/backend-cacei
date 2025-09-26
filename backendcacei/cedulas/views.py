from rest_framework import generics

from gestion_de_profesores.models import Profesor

from cedulas.serializers import CedulaCVSinteticoSerializer

# Create your views here.
class CedulaCVProfesorView(generics.RetrieveAPIView):
    queryset = Profesor.objects.all()
    serializer_class = CedulaCVSinteticoSerializer
