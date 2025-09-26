from rest_framework import routers

from evaluacion_acreditacion.views import (
    AccionMejoraViewSet,
    IndicadorViewSet,
    EvaluacionIndicadorViewSet,
    AportacionPEViewSet,
    GestionAcademicaViewSet,
    HallazgoViewSet,
    AuditoriaViewSet
)

router = routers.SimpleRouter()
router.register(r'acciones_mejora', AccionMejoraViewSet, basename='accion-mejora')
router.register(r'indicadores', IndicadorViewSet, basename='indicador')
router.register(r'evaluaciones_indicador', EvaluacionIndicadorViewSet, basename='evaluacion-indicador') 
router.register(r'aportaciones_pe', AportacionPEViewSet, basename='aportacion-pe')
router.register(r'gestion_academica', GestionAcademicaViewSet, basename='gestion-academica')
router.register(r'hallazgos', HallazgoViewSet, basename='hallazgo')
router.register(r'auditorias', AuditoriaViewSet, basename='auditoria')
urlpatterns = router.urls
