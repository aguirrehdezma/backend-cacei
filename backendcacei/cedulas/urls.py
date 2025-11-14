from rest_framework import routers

from cedulas.views import CedulaViewSet

router = routers.SimpleRouter()
router.register(r'', CedulaViewSet, basename='cedulas')
urlpatterns = router.urls
