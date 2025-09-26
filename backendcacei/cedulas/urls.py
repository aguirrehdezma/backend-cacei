from django.urls import path
from cedulas.views import CedulaCVSinteticoView, CedulaPlanMejoraView

urlpatterns = [
    path("profesor/<int:pk>/cv/", CedulaCVSinteticoView.as_view(), name="cedula-cv-sintetico"),
    path("hallazgo/<int:pk>/plan-mejora/", CedulaPlanMejoraView.as_view(), name="cedula-plan-mejora"),
]
