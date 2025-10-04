from django.urls import path
from usuarios_y_acceso.views import UsuariosView
from usuarios_y_acceso.views import UsuariosProgramasView

# Create your URLs here.

urlpatterns = [
    path('usuarios/', UsuariosView.as_view(), name='usuarios'),
    path('usuarios/<int:pk>/', UsuariosView.as_view(), name='profesoresusuarios-detail')
]

urlpatterns = [
    path('usuarios_cursos/', UsuariosProgramasView.as_view(), name='usuarios_cursos_cursos'),
    path('usuarios_cursos/<int:pk>/', UsuariosProgramasView.as_view(), name='usuarios_cursos-detail')
]
