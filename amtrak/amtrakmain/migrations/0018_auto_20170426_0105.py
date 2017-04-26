# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-26 01:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('amtrakmain', '0017_auto_20170424_2157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tickettrip',
            name='trip_date',
            field=models.DateField(blank=True, null=True, verbose_name='Trip Date'),
        ),
        migrations.AlterField(
            model_name='tickettrip',
            name='trip_fare',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Fare'),
        ),
        migrations.AlterField(
            model_name='tickettrip',
            name='trip_segment_end',
            field=models.ForeignKey(blank=True, help_text='Shows only north-end station of segment', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='s_end+', to='amtrakmain.Segment', verbose_name='Segment End'),
        ),
        migrations.AlterField(
            model_name='tickettrip',
            name='trip_segment_start',
            field=models.ForeignKey(blank=True, help_text='Shows only north-end station of segment', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='s_start+', to='amtrakmain.Segment', verbose_name='Segment Start'),
        ),
    ]