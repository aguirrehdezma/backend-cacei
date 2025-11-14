from django.contrib import admin

from cedulas.models import AccionMejoraCedula, ActualizacionDisciplinarCedula, AportacionPECedula, AtributoObjetivoCedula, AtributoPECACEICedula, AtributoPECedula, CapacitacionDocenteCedula, Cedula, CriterioDesempenoCedula, CursoObligatorio, CursoOptativo, EvaluacionIndicadorCedula, ExperienciaDisenoCedula, ExperienciaProfesionalCedula, FormacionAcademicaCedula, GestionAcademicaCedula, HallazgoCedula, IndicadorCedula, LogroProfesionalCedula, ObjetivoEducacionalCedula, ParticipacionOrganizacionesCedula, PremioDistincionCedula, ProductoAcademicoCedula

# Register your models here.
admin.site.register(Cedula)
admin.site.register(CursoObligatorio)
admin.site.register(CursoOptativo)
admin.site.register(ActualizacionDisciplinarCedula)
admin.site.register(FormacionAcademicaCedula)
admin.site.register(CapacitacionDocenteCedula)
admin.site.register(ExperienciaProfesionalCedula)
admin.site.register(ExperienciaDisenoCedula)
admin.site.register(LogroProfesionalCedula)
admin.site.register(ParticipacionOrganizacionesCedula)
admin.site.register(PremioDistincionCedula)
admin.site.register(ProductoAcademicoCedula)
admin.site.register(AportacionPECedula)
admin.site.register(GestionAcademicaCedula)
admin.site.register(HallazgoCedula)
admin.site.register(AccionMejoraCedula)
admin.site.register(ObjetivoEducacionalCedula)
admin.site.register(AtributoObjetivoCedula)
admin.site.register(CriterioDesempenoCedula)
admin.site.register(IndicadorCedula)
admin.site.register(EvaluacionIndicadorCedula)
admin.site.register(AtributoPECedula)
admin.site.register(AtributoPECACEICedula)
