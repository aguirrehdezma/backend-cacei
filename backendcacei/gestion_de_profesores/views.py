from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from usuarios_y_acceso.permissions import IsCoordinadorOrAdmin, IsDocenteOwner
from gestion_de_profesores.models import ActualizacionDisciplinar, CapacitacionDocente, ExperienciaDiseno, ExperienciaProfesional, FormacionAcademica, LogroProfesional, ParticipacionOrganizaciones, PremioDistincion, ProductoAcademico, ProfesorCurso
from gestion_de_profesores.serializers import ActualizacionDisciplinarSerializer, CapacitacionDocenteSerializer, ExperienciaDisenoSerializer, ExperienciaProfesionalSerializer, FormacionAcademicaSerializer, LogroProfesionalSerializer, ParticipacionOrganizacionesSerializer, PremioDistincionSerializer, ProductoAcademicoSerializer, ProfesorCursoSerializer

# Create your views here.
class ProfesorCursoViewSet(viewsets.ModelViewSet):
    queryset = ProfesorCurso.objects.all()
    serializer_class = ProfesorCursoSerializer
    permission_classes = [IsAuthenticated, IsCoordinadorOrAdmin]
    
    def get_queryset(self):
        user = self.request.user
        # Admin/Coordinador ven todo
        if user.role in ['admin', 'coordinador']:
            return ProfesorCurso.objects.all()
        # Docentes solo ven sus asignaciones (readonly)
        elif user.role == 'docente' and hasattr(user, 'profesor_profile'):
            return ProfesorCurso.objects.filter(profesor=user.profesor_profile)
        return ProfesorCurso.objects.none()

class FormacionAcademicaViewSet(viewsets.ModelViewSet):
    queryset = FormacionAcademica.objects.all()
    serializer_class = FormacionAcademicaSerializer
    permission_classes = [IsAuthenticated, IsDocenteOwner]
    
    def get_queryset(self):
        user = self.request.user
        if user.role in ['admin', 'coordinador']:
            return FormacionAcademica.objects.all()
        elif user.role == 'docente' and hasattr(user, 'profesor_profile'):
            return FormacionAcademica.objects.filter(profesor=user.profesor_profile)
        return FormacionAcademica.objects.none()
    
    def perform_create(self, serializer):
        # Si es docente, automáticamente asigna su profesor
        if self.request.user.role == 'docente' and hasattr(self.request.user, 'profesor_profile'):
            serializer.save(profesor=self.request.user.profesor_profile)
        else:
            serializer.save()

class ExperienciaProfesionalViewSet(viewsets.ModelViewSet):
    queryset = ExperienciaProfesional.objects.all()
    serializer_class = ExperienciaProfesionalSerializer
    permission_classes = [IsAuthenticated, IsDocenteOwner]
    
    def get_queryset(self):
        user = self.request.user
        if user.role in ['admin', 'coordinador']:
            return ExperienciaProfesional.objects.all()
        elif user.role == 'docente' and hasattr(user, 'profesor_profile'):
            return ExperienciaProfesional.objects.filter(profesor=user.profesor_profile)
        return ExperienciaProfesional.objects.none()
    
    def perform_create(self, serializer):
        if self.request.user.role == 'docente' and hasattr(self.request.user, 'profesor_profile'):
            serializer.save(profesor=self.request.user.profesor_profile)
        else:
            serializer.save()

class ExperienciaDisenoViewSet(viewsets.ModelViewSet):
    queryset = ExperienciaDiseno.objects.all()
    serializer_class = ExperienciaDisenoSerializer
    permission_classes = [IsAuthenticated, IsDocenteOwner]
    
    def get_queryset(self):
        user = self.request.user
        if user.role in ['admin', 'coordinador']:
            return ExperienciaDiseno.objects.all()
        elif user.role == 'docente' and hasattr(user, 'profesor_profile'):
            return ExperienciaDiseno.objects.filter(profesor=user.profesor_profile)
        return ExperienciaDiseno.objects.none()
    
    def perform_create(self, serializer):
        if self.request.user.role == 'docente' and hasattr(self.request.user, 'profesor_profile'):
            serializer.save(profesor=self.request.user.profesor_profile)
        else:
            serializer.save()

class LogroProfesionalViewSet(viewsets.ModelViewSet):
    queryset = LogroProfesional.objects.all()
    serializer_class = LogroProfesionalSerializer
    permission_classes = [IsAuthenticated, IsDocenteOwner]
    
    def get_queryset(self):
        user = self.request.user
        if user.role in ['admin', 'coordinador']:
            return LogroProfesional.objects.all()
        elif user.role == 'docente' and hasattr(user, 'profesor_profile'):
            return LogroProfesional.objects.filter(profesor=user.profesor_profile)
        return LogroProfesional.objects.none()
    
    def perform_create(self, serializer):
        if self.request.user.role == 'docente' and hasattr(self.request.user, 'profesor_profile'):
            serializer.save(profesor=self.request.user.profesor_profile)
        else:
            serializer.save()

class PremioDistincionViewSet(viewsets.ModelViewSet):
    queryset = PremioDistincion.objects.all()
    serializer_class = PremioDistincionSerializer
    permission_classes = [IsAuthenticated, IsDocenteOwner]
    
    def get_queryset(self):
        user = self.request.user
        if user.role in ['admin', 'coordinador']:
            return PremioDistincion.objects.all()
        elif user.role == 'docente' and hasattr(user, 'profesor_profile'):
            return PremioDistincion.objects.filter(profesor=user.profesor_profile)
        return PremioDistincion.objects.none()
    
    def perform_create(self, serializer):
        if self.request.user.role == 'docente' and hasattr(self.request.user, 'profesor_profile'):
            serializer.save(profesor=self.request.user.profesor_profile)
        else:
            serializer.save()

class ParticipacionOrganizacionesViewSet(viewsets.ModelViewSet):
    queryset = ParticipacionOrganizaciones.objects.all()
    serializer_class = ParticipacionOrganizacionesSerializer
    permission_classes = [IsAuthenticated, IsDocenteOwner]
    
    def get_queryset(self):
        user = self.request.user
        if user.role in ['admin', 'coordinador']:
            return ParticipacionOrganizaciones.objects.all()
        elif user.role == 'docente' and hasattr(user, 'profesor_profile'):
            return ParticipacionOrganizaciones.objects.filter(profesor=user.profesor_profile)
        return ParticipacionOrganizaciones.objects.none()
    
    def perform_create(self, serializer):
        if self.request.user.role == 'docente' and hasattr(self.request.user, 'profesor_profile'):
            serializer.save(profesor=self.request.user.profesor_profile)
        else:
            serializer.save()

class CapacitacionDocenteViewSet(viewsets.ModelViewSet):
    queryset = CapacitacionDocente.objects.all()
    serializer_class = CapacitacionDocenteSerializer
    permission_classes = [IsAuthenticated, IsDocenteOwner]
    
    def get_queryset(self):
        user = self.request.user
        if user.role in ['admin', 'coordinador']:
            return CapacitacionDocente.objects.all()
        elif user.role == 'docente' and hasattr(user, 'profesor_profile'):
            return CapacitacionDocente.objects.filter(profesor=user.profesor_profile)
        return CapacitacionDocente.objects.none()
    
    def perform_create(self, serializer):
        if self.request.user.role == 'docente' and hasattr(self.request.user, 'profesor_profile'):
            serializer.save(profesor=self.request.user.profesor_profile)
        else:
            serializer.save()

class ActualizacionDisciplinarViewSet(viewsets.ModelViewSet):
    queryset = ActualizacionDisciplinar.objects.all()
    serializer_class = ActualizacionDisciplinarSerializer
    permission_classes = [IsAuthenticated, IsDocenteOwner]
    
    def get_queryset(self):
        user = self.request.user
        if user.role in ['admin', 'coordinador']:
            return ActualizacionDisciplinar.objects.all()
        elif user.role == 'docente' and hasattr(user, 'profesor_profile'):
            return ActualizacionDisciplinar.objects.filter(profesor=user.profesor_profile)
        return ActualizacionDisciplinar.objects.none()
    
    def perform_create(self, serializer):
        if self.request.user.role == 'docente' and hasattr(self.request.user, 'profesor_profile'):
            serializer.save(profesor=self.request.user.profesor_profile)
        else:
            serializer.save()

class ProductoAcademicoViewSet(viewsets.ModelViewSet):
    queryset = ProductoAcademico.objects.all()
    serializer_class = ProductoAcademicoSerializer
    permission_classes = [IsAuthenticated, IsDocenteOwner]
    
    def get_queryset(self):
        user = self.request.user
        if user.role in ['admin', 'coordinador']:
            return ProductoAcademico.objects.all()
        elif user.role == 'docente' and hasattr(user, 'profesor_profile'):
            return ProductoAcademico.objects.filter(profesor=user.profesor_profile)
        return ProductoAcademico.objects.none()
    
    def perform_create(self, serializer):
        if self.request.user.role == 'docente' and hasattr(self.request.user, 'profesor_profile'):
            serializer.save(profesor=self.request.user.profesor_profile)
        else:
            serializer.save()
