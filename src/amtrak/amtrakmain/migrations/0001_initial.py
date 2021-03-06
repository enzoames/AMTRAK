# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-30 23:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Station',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('station_name', models.CharField(max_length=50, unique=True, verbose_name='Station Name')),
                ('station_symbol', models.CharField(max_length=5, unique=True, verbose_name='Station Symbol')),
            ],
        ),
    ]
