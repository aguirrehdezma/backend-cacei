from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from usuarios_y_acceso.serializers import (
    UserRegisterSerializer, 
    UserSerializer, 
    UserUpdateSerializer,
    ChangePasswordSerializer
)

from usuarios_y_acceso.models import CustomUser
from usuarios_y_acceso.permissions import IsAdmin

# Create your views here.
class RegisterView(generics.CreateAPIView):
    """
    Vista para registro de nuevos usuarios
    Abierta al público o puede ser restringida a admins según necesites
    """
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)  # Cambiar a (IsAdmin,) si solo admins pueden registrar
    serializer_class = UserRegisterSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        return Response({
            'message': 'Usuario registrado exitosamente',
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)

class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    Vista para ver y actualizar el perfil del usuario actual
    GET: Ver perfil completo
    PUT/PATCH: Actualizar datos básicos
    """
    permission_classes = (IsAuthenticated,)
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return UserUpdateSerializer
        return UserSerializer
    
    def get_object(self):
        return self.request.user

class ChangePasswordView(APIView):
    """
    Vista para cambiar la contraseña del usuario actual
    POST: Cambiar contraseña
    """
    permission_classes = (IsAuthenticated,)
    
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Contraseña actualizada exitosamente'
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserListView(generics.ListAPIView):
    """
    Vista para listar todos los usuarios (solo para admins)
    GET: Lista de usuarios con filtros
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # Filtros opcionales
        role = self.request.query_params.get('role', None)
        if role:
            queryset = queryset.filter(role=role)
        return queryset
