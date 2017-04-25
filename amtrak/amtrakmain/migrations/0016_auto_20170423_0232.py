# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-23 02:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('amtrakmain', '0015_auto_20170422_2329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tickettrip',
            name='trip_pay_method',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='t_pay', to='amtrakmain.PaymentMethod', verbose_name='Choose Payment'),
        ),
    ]
