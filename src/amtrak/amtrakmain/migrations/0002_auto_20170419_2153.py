# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-19 21:53
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('amtrakmain', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Passenger',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('p_f_name', models.CharField(max_length=15, verbose_name='First Name')),
                ('p_l_name', models.CharField(max_length=15, verbose_name='Last Name')),
                ('billing_address', models.CharField(max_length=50, verbose_name='Billing Address')),
                ('email', models.EmailField(default=0, max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=10, verbose_name='Type of payment')),
            ],
        ),
        migrations.CreateModel(
            name='Segment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seg_fare', models.IntegerField(default=0, verbose_name='Fare')),
                ('seg_north_end', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='n_end+', to='amtrakmain.Station', verbose_name='Segment North End')),
                ('seg_south_end', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='s_end+', to='amtrakmain.Station', verbose_name='Segment South End')),
            ],
        ),
        migrations.CreateModel(
            name='StopsAt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sa_time_in', models.DateField(verbose_name='Time-In of Train at Station')),
                ('sa_time_out', models.DateField(verbose_name='Time-out of train at Station')),
                ('sa_station', models.ManyToManyField(to='amtrakmain.Station', verbose_name='Station Where Train Stops')),
            ],
        ),
        migrations.CreateModel(
            name='TicketTrips',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trip_date', models.DateField(default=datetime.date.today, verbose_name='Trip Date')),
                ('trip_end', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='t_end+', to='amtrakmain.Station', verbose_name='Trip End Station')),
                ('trip_payment_method', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='amtrakmain.PaymentMethod', verbose_name='Choose Payment')),
                ('trip_segment_end', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='s_end+', to='amtrakmain.Segment', verbose_name='Segment End')),
                ('trip_segment_start', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='s_start+', to='amtrakmain.Segment', verbose_name='Segment Start')),
                ('trip_start', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='t_start+', to='amtrakmain.Station', verbose_name='Trip Start Station')),
            ],
        ),
        migrations.CreateModel(
            name='Train',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('train_direction', models.BooleanField(help_text='North = 1, South = 0')),
                ('train_days', models.CharField(help_text='M-T-W-Th-F-S-Su', max_length=13, verbose_name='Days train runs')),
                ('end_station', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='s_end', to='amtrakmain.Station', verbose_name='End Station')),
                ('start_station', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='s_start', to='amtrakmain.Station', verbose_name='Start Station')),
            ],
        ),
        migrations.AddField(
            model_name='tickettrips',
            name='trip_train',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='amtrakmain.Train', verbose_name='Train'),
        ),
        migrations.AddField(
            model_name='stopsat',
            name='sa_train',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='amtrakmain.Train', verbose_name='Which Train?'),
        ),
    ]
