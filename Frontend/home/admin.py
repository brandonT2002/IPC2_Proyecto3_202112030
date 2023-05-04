from django.contrib import admin
from . import models

# Register your models here.

class InfoAdmin(admin.ModelAdmin):
    list_display = ('root',)

admin.site.register(models.Archivo,InfoAdmin)