from __future__ import unicode_literals
from django.db import models
from datetime import date

# Create your models here
# MOST OF THE WORK WILL BE DONE HERE. Please read comments

# In models.py each class is a table in the database and each variable is a column




# ==== STATION ====
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



# ==== TRAIN ====
#
#   train_num     | start_station | train_ends | train_direction | train_days |
# ----------------|---------------|------------|-----------------|------------|
#   int auto pk   |  station_id   | station_id |     bool(S/N)   | what days this train runs |

class Train(models.Model):
    # 1-1 Field already unique by default
    start_station = models.OneToOneField(Station, related_name='s_start' ,verbose_name='Start Station')
    end_station = models.OneToOneField(Station, related_name='s_end', verbose_name='End Station')
    train_direction = models.BooleanField(help_text='North = 1, South = 0')
    train_days = models.CharField(max_length=13, verbose_name='Days train runs', help_text='M-T-W-Th-F-S-Su')

    def __unicode__(self):
        return self.start_station



# ==== PASSENGERS =====
#
#   passenger_id  | p_f_name | p_l_name | p_billing_address |   email    | points   |
# ----------------|----------|----------|-------------------|------------|----------|
#   int auto pk   |  VARCHAR | VARCHAR  |  emailField       | emailField |   ?      |

class Passenger(models.Model):
    p_f_name = models.CharField(max_length=15, verbose_name='First Name')
    p_l_name = models.CharField(max_length=15, verbose_name='Last Name')
    billing_address = models.CharField(max_length=50, verbose_name='Billing Address')
    email = models.EmailField(default=0)

    def __unicode__(self):
        return self.p_f_name



# ==== SEGMENTS ====
#
#   segment_id    | north_end     | south_end      | fares    | distance |
# ----------------|---------------|----------------|----------|
#   int auto pk   | station_id fk | station_id fk  | intField | ???

class Segment(models.Model):
    # A related_name argument is added to tell django to genrate unique names for them
    seg_north_end = models.ForeignKey(Station, related_name='n_end+', verbose_name='Segment North End')
    seg_south_end = models.ForeignKey(Station, related_name='s_end+', verbose_name='Segment South End')
    seg_fare = models.IntegerField(default=0, verbose_name='Fare')

    def __unicode__(self):
        return self.seg_fare



# ==== SEATS_FREE ====
#
#  seats_free_id  | sf_segment      | sf_date    |   sf_train_num    |
# ----------------|-----------------|------------|-------------------|
#   int auto pk   | segment_id *pk* |  dateField |    train_id *pk*  |

# class SeatsFree(models.Model):
# #     sf_segment = models.ForeignKey(Segment, related_name='seg+', verbose_name='Segment')
# #     sf_train = models.ForeignKey(Train, related_name='sf_train+', verbose_name='Train in Segment')
#     sf_date = models.DateField(verbose_name='Date')
# #
# #     # This allows us to create join together two columns
# #     class Meta:
# #         unique_together = (('sf_segment', 'sf_train'),)
# #
#     def __unicode__(self):
#         return self.sf_date



# ==== PAYMENT_METHOD ====
#
#   payment_id   | type      |
# ---------------|-----------|
#   int fk p_id  | VARCHAR   |

class PaymentMethod(models.Model):
    type = models.CharField(max_length=10, verbose_name='Type of payment')

    def __unicode__(self):
        return self.type



# ==== TRIPS ====
#
#   trip_id    | trip_start  | trip_end   | trip_train | fare | payment_method |
# -------------|-------------|------------|------------|------|----------------|
#  int auto pk | station_id  | station_id | train_id pk| int  | visa/master/   |
#
# trip_date | trip_seg_start  | trip_seg_end  |
# ----------|-----------------|---------------|
# dateField |  segment_id FK  | segment_id FK |

class TicketTrips(models.Model):
    trip_start = models.OneToOneField(Station, related_name='t_start+', verbose_name='Trip Start Station')
    trip_end = models.OneToOneField(Station, related_name='t_end+', verbose_name='Trip End Station')
    trip_train = models.OneToOneField(Train, verbose_name='Train')
    #fare = models.ForeignKey(Fare, verbose_name='Fare')
    trip_payment_method = models.OneToOneField(PaymentMethod, verbose_name='Choose Payment')
    trip_date = models.DateField(default=date.today, verbose_name='Trip Date')
    trip_segment_start = models.OneToOneField(Segment, related_name='s_start+', verbose_name='Segment Start')
    trip_segment_end = models.OneToOneField(Segment, related_name='s_end+', verbose_name='Segment End')

    def __unicode__(self):
        return self.trip_start



# # FARE ??? Do we need a table for fares ? not sure
# # get a reasonable fair between boston and washington and spread out the fares btw the segments
#
# #   fare_id   |   seg_start     | price |
# # ------------|-----------------|-------|
# # int auto pk |  segment_id FK  | int   |
#
#
# class Fare(models.Model):
#     fare_




# ==== STOPS_AT ====
#
#   train_num    | station_id      | time_in    | time_out  |
# ---------------|-----------------|------------|-----------|
#   int fk train | station_id fk   | time type  | time type |


class StopsAt(models.Model):
    sa_train = models.ForeignKey(Train, verbose_name='Which Train?')
    sa_station = models.ManyToManyField(Station, verbose_name='Station Where Train Stops')
    sa_time_in = models.DateField(verbose_name='Time-In of Train at Station')
    sa_time_out = models.DateField(verbose_name='Time-out of train at Station')

    def __unicode__(self):
        return self.sa_time_in



# https://data.cusp.nyu.edu/filebrowser/#/user/eames01





