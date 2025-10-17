from django.urls import path
from cedulas.views import CedulaCVSinteticoView, CedulaHerramientasValoracionAEPView, CedulaPlanMejoraView, CedulaProgramaAsignaturaView, CedulaValoracionOEPEView, CedulaOrganizacionCurricularView

urlpatterns = [
    path("profesores/<int:pk>/cv/", CedulaCVSinteticoView.as_view(), name="cedula-cv-sintetico"),
    path("hallazgos/<int:pk>/plan-mejora/", CedulaPlanMejoraView.as_view(), name="cedula-plan-mejora"),
    path("atributos-pe/<int:pk>/herramientas-valoracion-aep/", CedulaHerramientasValoracionAEPView.as_view(), name="cedula-herramientas-valoracion-aep"),
    path("cursos/<int:pk>/programa-curso-asignatura/", CedulaProgramaAsignaturaView.as_view(), name="cedula-programa-asignatura"),
    path("objetivos_educacionales/<int:pk>/valoracion_objetivos/", CedulaValoracionOEPEView.as_view(), name="cedula-valoracion-objetivos"),
    path("organizacion-curricular/<int:pk>/organizacion-curricular/", CedulaOrganizacionCurricularView.as_view(), name="cedula-organizacion-curricular"),
]
