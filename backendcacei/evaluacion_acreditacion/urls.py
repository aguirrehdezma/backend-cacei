from rest_framework import routers
from .views import AccionMejoraViewSet
from .views import IndicadorViewSet
from .views import EvaluacionIndicadorViewSet
from .views import AportacionPEViewSet
from .views import GestionAcademicaViewSet  
from .views import HallazgoViewSet 
from .views import AuditoriaViewSet






router = routers.SimpleRouter()
router.register(r'acciones_mejora', AccionMejoraViewSet, basename='accion-mejora')
router.register(r'indicadores', IndicadorViewSet, basename='indicador')
router.register(r'evaluaciones_indicador', EvaluacionIndicadorViewSet, basename='evaluacion-indicador') 
router.register(r'aportaciones_pe', AportacionPEViewSet, basename='aportacion-pe')
router.register(r'gestion_academica', GestionAcademicaViewSet, basename='gestion-academica')
router.register(r'hallazgos', HallazgoViewSet, basename='hallazgo')
router.register(r'auditorias', AuditoriaViewSet, basename='auditoria')
urlpatterns = router.urls

