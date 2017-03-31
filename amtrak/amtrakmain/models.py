from __future__ import unicode_literals
from django.db import models
from datetime import datetime

# Create your models here
# MOST OF THE WORK WILL BE DONE HERE. Please read comments

# In models.py each class is a table in the database and each variable is a column


# STATIONS
#
#   Station_id    | station_name | station_symbol |
# ----------------|--------------|----------------|
#   int auto pk   |  VARCHAR     | CHAR(3)        |

# Django automatically creates an auto increment primary key for every table, there is no need to specify it.

class Station(models.Model):
    station_name = models.CharField(unique=True, max_length=50, verbose_name='Station Name')
    station_symbol = models.CharField(unique=True, max_length=5, verbose_name='Station Symbol')

    def __unicode__(self):  # We need this function bc Django needs a reference to the database table Station
        return self.station_name  # station_name becomes the reference



# TRAINS
#
#   train_num     | starts_station | train_ends | train_direction | train_days |
# ----------------|----------------|------------|-----------------|------------|
#   int auto pk   |  station_id    | station_id |     bool(S/N)   | what days this train runs |


# PASSENGERS
#
#   passenger_id  | p_f_name | p_l_name | p_billing_address |   email    | points   |
# ----------------|----------|----------|-------------------|------------|----------|
#   int auto pk   |  VARCHAR | VARCHAR  |  emailField       | emailField |   ?      |


# SEATS_FREE
#
#  seats_free_id  | sf_segment    | sf_date    |   sf_train_num    |
# ----------------|---------------|------------|-------------------|
#   int auto pk   | segment_id pk |  dateField |    train_id pk    |


# PAYMENT_METHOD
#   - cash or credit


# TRIPS

#   trip_id    | trip_start  | trip_end   | trip_train | fare | payment_method |
# -------------|-------------|------------|------------|------|----------------|
#  int auto pk | station_id  | station_id | train_id pk| int  | visa/master/   |
#
# trip_date_from | trip_date_to   | trip_seg_start  | trip_seg_end  |
# ---------------|----------------|-----------------|---------------|
# dateField      | dateField/NULL |  segment_id FK  | segment_id FK |



# SEGMENTS/SECTIONS
#
#   segment_id    | north_end     | south_end      | fares    | distance |
# ----------------|---------------|----------------|----------|
#   int auto pk   | station_id fk | station_id fk  | intField |



# STOPS_AT
#
#   train_num    | station_id      | time_in    | time_out  |
# ---------------|-----------------|------------|-----------|
#   int fk train | station_id fk   | time type  | time type |



# FARE
#
# get a reasonable fair between boston and washington and spread out the fares btw the segments


