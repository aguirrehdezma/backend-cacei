from django.urls import path

from .views import UnidadTematicaList, UnidadTematicaDetail

urlpatterns = [
    path('list/', UnidadTematicaList.as_view(), name='unidad-tematica-list'),
    path('<int:pk>/', UnidadTematicaDetail.as_view(), name='unidad-tematica-detail'),
]
