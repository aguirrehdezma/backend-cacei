"""
URL configuration for backendcacei project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Autenticación y usuarios
    path('api/auth/', include('usuarios_y_acceso.urls')),
    
    # APIs de módulos
    path('api/core/', include('core.urls')),
    path('api/gestion_academica/', include('gestion_academica.urls')),
    path('api/evaluacion_acreditacion/', include('evaluacion_acreditacion.urls')),
    path('api/gestion_de_profesores/', include('gestion_de_profesores.urls')),
    path('api/cedulas/', include('cedulas.urls')),
]