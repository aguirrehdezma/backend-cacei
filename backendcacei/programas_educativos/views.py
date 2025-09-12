from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from programas_educativos.models import ProgramaEducativo
from programas_educativos.serializers import ProgramaEducativoSerializer

# Create your views here.
class ProgramaEducativoList(APIView):
    def get(self, request):
        programas = ProgramaEducativo.objects.all()
        serializer = ProgramaEducativoSerializer(programas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = ProgramaEducativoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ProgramaEducativoDetail(APIView):
    def get(self, request, pk):
        try:
            programa = ProgramaEducativo.objects.get(pk=pk)
        except ProgramaEducativo.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = ProgramaEducativoSerializer(programa)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        try:
            programa = ProgramaEducativo.objects.get(pk=pk)
        except ProgramaEducativo.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = ProgramaEducativoSerializer(programa, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        try:
            programa = ProgramaEducativo.objects.get(pk=pk)
        except ProgramaEducativo.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        programa.estatus = ProgramaEducativo.INACTIVO
        programa.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
