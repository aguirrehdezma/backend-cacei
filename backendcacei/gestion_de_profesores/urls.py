from rest_framework import routers

from gestion_de_profesores.views import ActualizacionDisciplinarViewSet, CapacitacionDocenteViewSet, ExperienciaDisenoViewSet, ExperienciaProfesionalViewSet, FormacionAcademicaViewSet, LogroProfesionalViewSet, ParticipacionOrganizacionesViewSet, PremioDistincionViewSet, ProductoAcademicoViewSet, ProfesorCursoViewSet

router = routers.SimpleRouter()
router.register(r'profesores_cursos', ProfesorCursoViewSet, basename='profesor-curso')
router.register(r'formacion_academica', FormacionAcademicaViewSet, basename='formacion-academica')
router.register(r'experiencia_profesional', ExperienciaProfesionalViewSet, basename='experiencia-profesional')
router.register(r'experiencia_diseno', ExperienciaDisenoViewSet, basename='experiencia-diseno')
router.register(r'logros_profesionales', LogroProfesionalViewSet, basename='logro-profesional')
router.register(r'premios_distincion', PremioDistincionViewSet, basename='premio-distincion')
router.register(r'participacion_organizaciones', ParticipacionOrganizacionesViewSet, basename='participacion-organizaciones')
router.register(r'capacitacion_docente', CapacitacionDocenteViewSet, basename='capacitacion-docente')
router.register(r'actualizacion_disciplinar', ActualizacionDisciplinarViewSet, basename='actualizacion-disciplinar')
router.register(r'productos_academicos', ProductoAcademicoViewSet, basename='producto-academico')
urlpatterns = router.urls
