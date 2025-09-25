from django.urls import path
from gestion_de_profesores.views import ProfesoresView
from gestion_de_profesores.views import ProfesoresCursosView
from gestion_de_profesores.views import FormacionAcademicaView
from gestion_de_profesores.views import ExperienciaProfesionalView
from gestion_de_profesores.views import ExperienciaDisenoView
from gestion_de_profesores.views import LogrosProfesionalesView
from gestion_de_profesores.views import PremiosDistincionesView
from gestion_de_profesores.views import ParticipacionOrganizacionesView
from gestion_de_profesores.views import CapacitacionDocenteView
from gestion_de_profesores.views import ActualizacionDisciplinarView
from gestion_de_profesores.views import ProductoAcademicoView

# Create your URLs here.

urlpatterns = [
    path('profesores/', ProfesoresView.as_view(), name='profesores'),
    path('profesores/<int:pk>/', ProfesoresView.as_view(), name='profesores-detail')
]

urlpatterns = [
    path('profesores_cursos/', ProfesoresCursosView.as_view(), name='profesores_cursos'),
    path('profesores_cursos/<int:pk>/', ProfesoresCursosView.as_view(), name='profesores_cursos-detail')
]

urlpatterns = [
    path('formacion_academica/', FormacionAcademicaView.as_view(), name='formacion_academica'),
    path('formacion_academica/<int:pk>/', FormacionAcademicaView.as_view(), name='formacion_academica-detail')
]

urlpatterns = [
    path('experiencia_profesional/', ExperienciaProfesionalView.as_view(), name='experiencia_profesional'),
    path('experiencia_profesional/<int:pk>/', ExperienciaProfesionalView.as_view(), name='experiencia_profesional-detail')
]


urlpatterns = [
    path('experiencia_diseno/', ExperienciaDisenoView.as_view(), name='experiencia_diseno'),
    path('experiencia_diseno/<int:pk>/', ExperienciaDisenoView.as_view(), name='experiencia_diseno-detail')
]


urlpatterns = [
    path('logros_profesionales/', LogrosProfesionalesView.as_view(), name='logros_profesionales'),
    path('logros_profesionales/<int:pk>/', LogrosProfesionalesView.as_view(), name='logros_profesionales-detail')
]


urlpatterns = [
    path('formacion_academica/', FormacionAcademicaView.as_view(), name='formacion_academica'),
    path('formacion_academica/<int:pk>/', FormacionAcademicaView.as_view(), name='formacion_academica-detail')
]


urlpatterns = [
    path('premios_distinciones/', PremiosDistincionesView.as_view(), name='premios_distinciones'),
    path('premios_distinciones/<int:pk>/', PremiosDistincionesView.as_view(), name='premios_distinciones-detail')
]


urlpatterns = [
    path('actualizacion_disciplinar/', ActualizacionDisciplinarView.as_view(), name='actualizacion_disciplinar'),
    path('actualizacion_disciplinar/<int:pk>/', ActualizacionDisciplinarView.as_view(), name='actualizacion_disciplinar-detail')
]


urlpatterns = [
    path('participacion_organizaciones/', ParticipacionOrganizacionesView.as_view(), name='participacion_organizaciones'),
    path('participacion_organizaciones/<int:pk>/', ParticipacionOrganizacionesView.as_view(), name='participacion_organizaciones-detail')
]


urlpatterns = [
    path('capacitacion_docente/', CapacitacionDocenteView.as_view(), name='capacitacion_docente'),
    path('capacitacion_docente/<int:pk>/', CapacitacionDocenteView.as_view(), name='capacitacion_docente-detail')
]

urlpatterns = [
    path('producto_academico/', ProductoAcademicoView.as_view(), name='producto_academico'),
    path('producto_academico/<int:pk>/', ProductoAcademicoView.as_view(), name='producto_academico-detail')
]
