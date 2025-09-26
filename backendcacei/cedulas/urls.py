from django.urls import path
from cedulas.views import CedulaCVProfesorView

urlpatterns = [
    path("profesor/<int:pk>/cv/", CedulaCVProfesorView.as_view(), name="cedula-cv-profesor"),
]
