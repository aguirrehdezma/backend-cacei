from django.contrib import admin

from cedulas.models import Cedula, CursoObligatorio, CursoOptativo

# Register your models here.
admin.site.register(Cedula)
admin.site.register(CursoObligatorio)
admin.site.register(CursoOptativo)
