# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-20 19:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amtrakmain', '0003_auto_20170420_1954'),
    ]

    operations = [
        migrations.AlterField(
            model_name='train',
            name='train_number',
            field=models.CharField(max_length=15, verbose_name='Train Number'),
        ),
    ]
