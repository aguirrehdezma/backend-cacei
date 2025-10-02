from django.contrib import admin

from core.models import Curso, Profesor, ProgramaEducativo

# Register your models here.
admin.site.register(Profesor)
admin.site.register(ProgramaEducativo)
admin.site.register(Curso)
