from django.contrib import admin

from core.models import Curso, Institucion, Organizacion, Periodo, Profesor, ProgramaEducativo

# Register your models here.
admin.site.register(Profesor)
admin.site.register(ProgramaEducativo)
admin.site.register(Curso)
admin.site.register(Institucion)
admin.site.register(Organizacion)
admin.site.register(Periodo)
