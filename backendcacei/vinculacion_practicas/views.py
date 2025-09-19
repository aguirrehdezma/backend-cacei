from django.shortcuts import render
from rest_framework import viewsets
from .models import Practica
from .serializers import PracticaSerializer

# Create your views here.

class PracticaViewSet(viewsets.ModelViewSet):
    from .models import Practica
    from .serializers import PracticaSerializer

    queryset = Practica.objects.all()
    serializer_class = PracticaSerializer

    