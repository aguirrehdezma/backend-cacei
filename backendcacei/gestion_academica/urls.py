from rest_framework import routers

from gestion_academica.views import AtributoCACEIViewSet, AtributoPEViewSet, BibliografiaViewSet, CriterioDesempenoViewSet, CursoViewSet, EjeConocimientoViewSet, EstrategiaEnsenanzaViewSet, EstrategiaEvaluacionViewSet, HorasSemanaViewSet, ObjetivoEducacionalViewSet, ObjetivoEspecificoViewSet, ProgramaEducativoViewSet, UnidadTematicaViewSet

router = routers.SimpleRouter()
router.register(r'programas_educativos', ProgramaEducativoViewSet, basename='programa-educativo')
router.register(r'unidades_tematicas', UnidadTematicaViewSet, basename='unidad-tematica')
router.register(r'criterios_desempeno', CriterioDesempenoViewSet, basename='criterio-desempeno')
router.register(r'cursos', CursoViewSet, basename='curso')
router.register(r'estrategias_ensenanza', EstrategiaEnsenanzaViewSet, basename='estrategia-ensenanza')
router.register(r'estrategias_evaluacion', EstrategiaEvaluacionViewSet, basename='estrategia-evaluacion')
router.register(r'objetivos_educacionales', ObjetivoEducacionalViewSet, basename='objetivo-educacional')
router.register(r'bibliografia', BibliografiaViewSet, basename='bibliografia')
router.register(r'horas_semana', HorasSemanaViewSet, basename='horas-semana')
router.register(r'ejes_conocimiento', EjeConocimientoViewSet, basename='eje-conocimiento')
router.register(r'objetivos_especificos', ObjetivoEspecificoViewSet, basename='objetivo-especifico')
router.register(r'atributos_pe', AtributoPEViewSet, basename='atributo-pe')
router.register(r'atributos_cacei', AtributoCACEIViewSet, basename='atributo-cacei')
urlpatterns = router.urls
