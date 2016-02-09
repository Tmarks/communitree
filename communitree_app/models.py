from __future__ import unicode_literals

from django.contrib.gis.db import models
from django.utils import timezone

# Create your models here.


class USDAZone(models.Model):
    name = models.CharField(max_length=3, default="1", unique=True)


class Species(models.Model):
    scientific_name = models.CharField(max_length=100)
    common_name = models.CharField(max_length=70)
    usda_zones = models.ManyToManyField(USDAZone)


class CropFeature(models.Model):
    name = models.CharField(max_length=30)
    species = models.ForeignKey("Species", null=True)
    mpoly = models.MultiPolygonField()


class Pruning(models.Model):
    cropfeature = models.ForeignKey(CropFeature, on_delete=models.CASCADE)
    log_time = models.DateTimeField(default=timezone.now)
    completion_percentage = models.DecimalField(max_digits=3, decimal_places=2)
