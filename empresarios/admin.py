from django.contrib import admin

# Register your models here.
from . import models

admin.site.register(models.Empresas)
admin.site.register(models.Documento)
admin.site.register(models.Metricas)
