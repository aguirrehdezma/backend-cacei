from django.shortcuts import render
from rest_framework import viewsets
from .models import AccionMejora
from .serializers import AccionMejoraSerializer
from .models import Indicador
from .serializers import IndicadorSerializer

# Create your views here.
class AccionMejoraViewSet(viewsets.ModelViewSet):
    queryset = AccionMejora.objects.all()
    serializer_class = AccionMejoraSerializer

class IndicadorViewSet(viewsets.ModelViewSet):
    queryset = Indicador.objects.all()
    serializer_class = IndicadorSerializer