from __future__ import unicode_literals

from django.contrib.gis.db import models
from django.utils import timezone

# Create your models here.


class CropFeature(models.Model):
    name = models.CharField(max_length=30)
    species = models.NullBooleanField()
    mpoly = models.MultiPolygonField()


class Pruning(models.Model):
    crop_feature = models.ForeignKey(CropFeature, on_delete=models.CASCADE)
    log_time = models.DateTimeField(default=timezone.now)
    completion_percentage = models.DecimalField(max_digits=3, decimal_places=2)


class Species(models.Model):
    scientific_name = models.CharField(max_length=100)
    common_name = models.CharField(max_length=70)
    usda_zone = models.CharField(max_length=2)


