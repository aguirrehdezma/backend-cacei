from django.urls import path

from .views import CriterioDesempenoList, CriterioDesempenoDetail

urlpatterns = [
    path('list/', CriterioDesempenoList.as_view(), name='criterio-desempeno-list'),
    path('<int:pk>/', CriterioDesempenoDetail.as_view(), name='criterio-desempeno-detail'),
]
