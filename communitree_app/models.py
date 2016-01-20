from __future__ import unicode_literals

from django.contrib.gis.db import models

# Create your models here.

class CropFeature(models.Model):
    name=models.CharField(max_length=30)
    species=models.NullBooleanField()
    mpoly=models.MultiPolygonField()
    

