# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-26 01:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('amtrakmain', '0014_auto_20170422_2236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tickettrip',
            name='trip_date',
            field=models.DateField(verbose_name='Trip Date'),
        ),
        migrations.AlterField(
            model_name='tickettrip',
            name='trip_pay_method',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='t_pay', to='amtrakmain.PaymentMethod', verbose_name='Choose Payment'),
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
        migrations.AlterField(
            model_name='tickettrip',
            name='trip_train',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='amtrakmain.Train', verbose_name='Train'),
        ),
    ]