# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-13 22:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('communitree_app', '0017_auto_20160304_0327'),
    ]

    operations = [
        migrations.AddField(
            model_name='cropfeature',
            name='active_pruning_event',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cropfeature_active', to='communitree_app.PruningEvent'),
        ),
    ]
