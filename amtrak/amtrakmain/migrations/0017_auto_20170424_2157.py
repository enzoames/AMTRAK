# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-24 21:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amtrakmain', '0016_auto_20170423_0232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tickettrip',
            name='trip_date',
            field=models.DateTimeField(verbose_name='Trip Date'),
        ),
    ]
