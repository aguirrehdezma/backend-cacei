from rest_framework import routers

from cedulas.views import CedulaViewSet, CursoObligatorioViewSet, CursoOptativoViewSet

router = routers.SimpleRouter()
router.register(r'', CedulaViewSet, basename='cedulas')
router.register(r'cursos_obligatorios', CursoObligatorioViewSet, basename='curso-obligatorio')
router.register(r'cursos_optativos', CursoOptativoViewSet, basename='curso-optativo')
urlpatterns = router.urls
