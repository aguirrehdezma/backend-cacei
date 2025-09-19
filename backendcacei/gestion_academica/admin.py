from django.contrib import admin

from gestion_academica.models import Bibliografia, CriterioDesempeno, Curso, EstrategiaEnsenanza, EstrategiaEvaluacion, HorasSemana, ObjetivoEducacional, ProductoAcademico, ProgramaEducativo, UnidadTematica

# Register your models here.
admin.site.register(ProgramaEducativo)
admin.site.register(UnidadTematica)
admin.site.register(CriterioDesempeno)
admin.site.register(Curso)
admin.site.register(EstrategiaEnsenanza)
admin.site.register(EstrategiaEvaluacion)
admin.site.register(ObjetivoEducacional)
admin.site.register(Bibliografia)
admin.site.register(HorasSemana)
admin.site.register(ProductoAcademico)
