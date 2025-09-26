from rest_framework import routers

from vinculacion_practicas.views import PracticaViewSet

router = routers.SimpleRouter()
router.register(r'practicas', PracticaViewSet, basename='practicas')
urlpatterns = router.urls
