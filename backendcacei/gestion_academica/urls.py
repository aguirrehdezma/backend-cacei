from rest_framework import routers

from gestion_academica.views import CriterioDesempenoViewSet, CursoViewSet, EstrategiaEnsenanzaViewSet, ProgramaEducativoViewSet, UnidadTematicaViewSet

router = routers.SimpleRouter()
router.register(r'programas_educativos', ProgramaEducativoViewSet, basename='programa-educativo')
router.register(r'unidades_tematicas', UnidadTematicaViewSet, basename='unidad-tematica')
router.register(r'criterios_desempeno', CriterioDesempenoViewSet, basename='criterio-desempeno')
router.register(r'cursos', CursoViewSet, basename='curso')
router.register(r'estrategias_ensenanza', EstrategiaEnsenanzaViewSet, basename='estrategia-ensenanza')
urlpatterns = router.urls
