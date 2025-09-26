from django.contrib import admin

from evaluacion_acreditacion.models import AccionMejora, AportacionPE, Auditoria, EvaluacionIndicador, GestionAcademica, Hallazgo, Indicador

# Register your models here.
admin.site.register(AccionMejora)
admin.site.register(Indicador)
admin.site.register(EvaluacionIndicador)
admin.site.register(AportacionPE)
admin.site.register(GestionAcademica)
admin.site.register(Hallazgo)
admin.site.register(Auditoria)
