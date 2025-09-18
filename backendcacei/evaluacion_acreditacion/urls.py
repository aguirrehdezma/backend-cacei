from rest_framework import routers
from .views import AccionMejoraViewSet
from .views import IndicadorViewSet


router = routers.SimpleRouter()
router.register(r'acciones_mejora', AccionMejoraViewSet, basename='accion-mejora')
router.register(r'indicadores', IndicadorViewSet, basename='indicador')
urlpatterns = router.urls

