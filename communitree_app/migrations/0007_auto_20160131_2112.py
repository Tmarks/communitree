# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-31 21:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('communitree_app', '0006_auto_20160131_2104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usdazone',
            name='name',
            field=models.CharField(default='1', max_length=3, unique=True),
        ),
    ]
