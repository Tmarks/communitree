# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-04 02:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('communitree_app', '0015_auto_20160303_2257'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pruning',
            name='pruningevent',
        ),
        migrations.AddField(
            model_name='pruning',
            name='cropfeature',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='communitree_app.CropFeature'),
            preserve_default=False,
        ),
    ]
