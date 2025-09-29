from django.contrib import admin

from gestion_academica.models import AtributoCACEI, AtributoPE, AtributoPECACEI, AtributoPEObjetivo, Bibliografia, CriterioDesempeno, Curso, CursoAtributoPE, CursoEje, EjeConocimiento, EstrategiaEnsenanza, EstrategiaEvaluacion, HorasSemana, ObjetivoEducacional, ObjetivoEspecifico, ProgramaEducativo, UnidadTematica

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
admin.site.register(EjeConocimiento)
admin.site.register(ObjetivoEspecifico)
admin.site.register(AtributoPE)
admin.site.register(AtributoCACEI)
admin.site.register(CursoAtributoPE)
admin.site.register(CursoEje)
admin.site.register(AtributoPEObjetivo)
admin.site.register(AtributoPECACEI)
