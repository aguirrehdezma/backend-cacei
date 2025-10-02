from rest_framework import routers

from gestion_academica.views import AtributoCACEIViewSet, AtributoPECACEIViewSet, AtributoPEObjetivoViewSet, AtributoPEViewSet, BibliografiaViewSet, CriterioDesempenoViewSet, CursoAtributoPEViewSet, CursoEjeViewSet, EjeConocimientoViewSet, EstrategiaEnsenanzaViewSet, EstrategiaEvaluacionViewSet, HorasSemanaViewSet, ObjetivoEducacionalViewSet, ObjetivoEspecificoViewSet, PracticaViewSet, UnidadTematicaViewSet

router = routers.SimpleRouter()
router.register(r'unidades_tematicas', UnidadTematicaViewSet, basename='unidad-tematica')
router.register(r'criterios_desempeno', CriterioDesempenoViewSet, basename='criterio-desempeno')
router.register(r'estrategias_ensenanza', EstrategiaEnsenanzaViewSet, basename='estrategia-ensenanza')
router.register(r'estrategias_evaluacion', EstrategiaEvaluacionViewSet, basename='estrategia-evaluacion')
router.register(r'objetivos_educacionales', ObjetivoEducacionalViewSet, basename='objetivo-educacional')
router.register(r'bibliografia', BibliografiaViewSet, basename='bibliografia')
router.register(r'horas_semana', HorasSemanaViewSet, basename='horas-semana')
router.register(r'ejes_conocimiento', EjeConocimientoViewSet, basename='eje-conocimiento')
router.register(r'objetivos_especificos', ObjetivoEspecificoViewSet, basename='objetivo-especifico')
router.register(r'atributos_pe', AtributoPEViewSet, basename='atributo-pe')
router.register(r'atributos_cacei', AtributoCACEIViewSet, basename='atributo-cacei')
router.register(r'cursos_atributos_pe', CursoAtributoPEViewSet, basename='curso-atributo-pe')
router.register(r'cursos_ejes', CursoEjeViewSet, basename='curso-eje')
router.register(r'atributos_pe_objetivos', AtributoPEObjetivoViewSet, basename='atributo-pe-objetivo')
router.register(r'atributos_pe_cacei', AtributoPECACEIViewSet, basename='atributo-pe-cacei')
router.register(r'practicas', PracticaViewSet, basename='practica')
urlpatterns = router.urls
