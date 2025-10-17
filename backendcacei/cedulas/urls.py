from django.urls import path

from cedulas.views import CedulaAEPVsAECACEIView, CedulaAEPVsOEView, CedulaCVSinteticoView, CedulaCursosVsAEPView, CedulaHerramientasValoracionAEPView, CedulaPlanMejoraView, CedulaProgramaAsignaturaView, CedulaValoracionOEPEView, CedulaOrganizacionCurricularView

urlpatterns = [
    path("profesores/<int:pk>/cv/", CedulaCVSinteticoView.as_view(), name="cedula-cv-sintetico"),
    path("hallazgos/<int:pk>/plan-mejora/", CedulaPlanMejoraView.as_view(), name="cedula-plan-mejora"),
    path("atributos-pe/<int:pk>/herramientas-valoracion-aep/", CedulaHerramientasValoracionAEPView.as_view(), name="cedula-herramientas-valoracion-aep"),
    path("cursos/<int:pk>/programa-curso-asignatura/", CedulaProgramaAsignaturaView.as_view(), name="cedula-programa-asignatura"),
    path("objetivos_educacionales/<int:pk>/valoracion_objetivos/", CedulaValoracionOEPEView.as_view(), name="cedula-valoracion-objetivos"),
    path("programas_educativos/<int:pk>/organizacion_curricular/", CedulaOrganizacionCurricularView.as_view(), name="cedula-organizacion-curricular"),
    path("programas_educativos/<int:pk>/cursos_vs_aep/", CedulaCursosVsAEPView.as_view(), name="cedula-cursos-vs-aep"),
    path("programas_educativos/<int:pk>/aep_vs_aecacei/", CedulaAEPVsAECACEIView.as_view(), name="cedula-aep-vs-aecacei"),
    path("programas_educativos/<int:pk>/aep_vs_oe/", CedulaAEPVsOEView.as_view(), name="cedula-aep-vs-oe"),
]
