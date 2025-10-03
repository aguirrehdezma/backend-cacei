from django.urls import path
from cedulas.views import CedulaCVSinteticoView, CedulaHerramientasValoracionAEPView, CedulaPlanMejoraView, CedulaProgramacursoasignaturaView, CedulaValoracionObjetivosView

urlpatterns = [
    path("profesores/<int:pk>/cv/", CedulaCVSinteticoView.as_view(), name="cedula-cv-sintetico"),
    path("hallazgos/<int:pk>/plan-mejora/", CedulaPlanMejoraView.as_view(), name="cedula-plan-mejora"),
    path("atributos-pe/<int:pk>/herramientas-valoracion-aep/", CedulaHerramientasValoracionAEPView.as_view(), name="cedula-herramientas-valoracion-aep"),
    path("cursos/<int:pk>/programa-curso-asignatura/", CedulaProgramacursoasignaturaView.as_view(), name="cedula-programa-curso-asignatura"),
    path("objetivos-educacionales/<int:pk>/valoracion-objetivos/", CedulaValoracionObjetivosView.as_view(), name="cedula-valoracion-objetivos"),


]
