from rest_framework import viewsets

from vinculacion_practicas.models import Practica
from vinculacion_practicas.serializers import PracticaSerializer

# Create your views here.
class PracticaViewSet(viewsets.ModelViewSet):
    queryset = Practica.objects.all()
    serializer_class = PracticaSerializer
