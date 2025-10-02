from rest_framework import routers

from core.views import CursoViewSet, ProfesorViewSet, ProgramaEducativoViewSet

router = routers.SimpleRouter()
router.register(r'profesores', ProfesorViewSet, basename='profesor')
router.register(r'programas_educativos', ProgramaEducativoViewSet, basename='programa-educativo')
router.register(r'cursos', CursoViewSet, basename='curso')
urlpatterns = router.urls
