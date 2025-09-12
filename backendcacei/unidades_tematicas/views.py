from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from unidades_tematicas.models import UnidadTematica
from unidades_tematicas.serializers import UnidadTematicaSerializer

# Create your views here.
class UnidadTematicaList(APIView):
    def get(self, request):
        unidades = UnidadTematica.objects.all()
        serializer = UnidadTematicaSerializer(unidades, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = UnidadTematicaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UnidadTematicaDetail(APIView):
    def get(self, request, pk):
        try:
            unidad = UnidadTematica.objects.get(pk=pk)
        except UnidadTematica.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = UnidadTematicaSerializer(unidad)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        try:
            unidad = UnidadTematica.objects.get(pk=pk)
        except UnidadTematica.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = UnidadTematicaSerializer(unidad, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        try:
            unidad = UnidadTematica.objects.get(pk=pk)
        except UnidadTematica.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        unidad.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
