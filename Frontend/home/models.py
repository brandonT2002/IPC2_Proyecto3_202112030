from django.db import models
# Create your models here.

class Archivo(models.Model):
    root = models.CharField(max_length = 200)
    content = models.TextField(null = True)
    response = models.TextField(null = True)