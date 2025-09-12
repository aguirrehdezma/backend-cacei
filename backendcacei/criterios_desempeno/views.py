from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from criterios_desempeno.models import CriterioDesempeno
from criterios_desempeno.serializers import CriterioDesempenoSerializer

# Create your views here.
class CriterioDesempenoList(APIView):
    def get(self, request):
        criterios = CriterioDesempeno.objects.all()
        serializer = CriterioDesempenoSerializer(criterios, many=True)
        return Response(serializer.data, statsus=status.HTTP_200_OK)

    def post(self, request):
        serializer = CriterioDesempenoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CriterioDesempenoDetail(APIView):
    def get(self, request, pk):
        try:
            criterio = CriterioDesempeno.objects.get(pk=pk)
        except CriterioDesempeno.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = CriterioDesempenoSerializer(criterio)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        try:
            criterio = CriterioDesempeno.objects.get(pk=pk)
        except CriterioDesempeno.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = CriterioDesempenoSerializer(criterio, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        try:
            criterio = CriterioDesempeno.objects.get(pk=pk)
        except CriterioDesempeno.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        criterio.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)