from django.urls import path

from .views import ProgramaEducativoList, ProgramaEducativoDetail

urlpatterns = [
    path('list/', ProgramaEducativoList.as_view(), name='programa-educativo-list'),
    path('<int:pk>/', ProgramaEducativoDetail.as_view(), name='programa-educativo-detail'),
]
