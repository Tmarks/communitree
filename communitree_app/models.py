from __future__ import unicode_literals

from django.contrib.gis.db import models
from django.utils import timezone
from datetime import datetime, timedelta

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
    """A Pruning event, done by a user of the system.

    When a user decides to prune a crop, they will estimate how much of the
    work they've done and tell Communitree. A Pruning is created on that
    CropFeature to log it.
    """
    cropfeature = models.ForeignKey(CropFeature, on_delete=models.CASCADE)
    log_time = models.DateTimeField(default=timezone.now)
    completion_percentage = models.DecimalField(max_digits=3, decimal_places=2)


class PruningEvent(models.Model):
    cropfeature = models.ForeignKey(CropFeature, on_delete=models.CASCADE)
    start_time = models.DateTimeField(default=timezone.now)
