from django.contrib import admin

from cedulas.models import ActualizacionDisciplinarCedula, AportacionPECedula, CapacitacionDocenteCedula, Cedula, CursoObligatorio, CursoOptativo, ExperienciaDisenoCedula, ExperienciaProfesionalCedula, FormacionAcademicaCedula, GestionAcademicaCedula, LogroProfesionalCedula, ParticipacionOrganizacionesCedula, PremioDistincionCedula, ProductoAcademicoCedula

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
