from django.contrib import admin

from gestion_de_profesores.models import ActualizacionDisciplinar, CapacitacionDocente, ExperienciaDiseno, ExperienciaProfesional, FormacionAcademica, LogroProfesional, ParticipacionOrganizaciones, PremioDistincion, Profesor, ProfesorCurso

# Register your models here.
admin.site.register(Profesor)
admin.site.register(ProfesorCurso)
admin.site.register(FormacionAcademica)
admin.site.register(ExperienciaProfesional)
admin.site.register(ExperienciaDiseno)
admin.site.register(LogroProfesional)
admin.site.register(PremioDistincion)
admin.site.register(ParticipacionOrganizaciones)
admin.site.register(CapacitacionDocente)
admin.site.register(ActualizacionDisciplinar)
