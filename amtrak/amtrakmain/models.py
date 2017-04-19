from __future__ import unicode_literals
from django.db import models
from datetime import datetime

# Create your models here
# MOST OF THE WORK WILL BE DONE HERE. Please read comments

# In models.py each class is a table in the database and each variable is a column


                                    # ====================================
                                    # ============ ENTITIES ==============
                                    # ====================================


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
    start_station = models.ForeignKey(Station, verbose_name='Train starts at Station')
    end_station = models.ForeignKey(Station, verbose_name='Train ends at Station')
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

# ==== SEATS_FREE ====
#
#  seats_free_id  | sf_segment    | sf_date    |   sf_train_num    |
# ----------------|---------------|------------|-------------------|
#   int auto pk   | segment_id pk |  dateField |    train_id pk    |

class SeatsFree(models.Model):
    sf_segment = models.ForeignKey(Segment, primary_key=True)
    sf_train = models.ForeignKey(Train, primary_key=True)
    sf_date = models.DateField(verbose_name='Date')

    def __unicode__(self):
        return self.sf_date


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
# trip_date_from | trip_date_to   | trip_seg_start  | trip_seg_end  |
# ---------------|----------------|-----------------|---------------|
# dateField      | dateField/NULL |  segment_id FK  | segment_id FK |

class TicketTrips(models.Model):
    trip_start = models.ForeignKey(Station, verbose_name='Trip Start Station') # unique true ?
    trip_end = models.ForeignKey(Station, verbose_name='Trip End Station') # unique true ?
    trip_train = models.ForeignKey(Train, verbose_name='Train')
    fare = models.ForeignKey(Fare, verbose_name='Fare')
    trip_payment_method = models.ForeignKey(PaymentMethod, verbose_name='Choose Payment')
    trip_date = models.ForeignKey() 


# FARE
#
# get a reasonable fair between boston and washington and spread out the fares btw the segments

                                    # ====================================
                                    # ============ RELATIONS =============
                                    # ====================================

# STOPS_AT
#
#   train_num    | station_id      | time_in    | time_out  |
# ---------------|-----------------|------------|-----------|
#   int fk train | station_id fk   | time type  | time type |



# SEGMENTS/SECTIONS
#
#   segment_id    | north_end     | south_end      | fares    | distance |
# ----------------|---------------|----------------|----------|
#   int auto pk   | station_id fk | station_id fk  | intField |






