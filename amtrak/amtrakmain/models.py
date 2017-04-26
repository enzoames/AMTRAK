from __future__ import unicode_literals
from django.db import models
from datetime import date
from django.core.validators import MaxValueValidator

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
    station_name = models.CharField(unique=True, max_length=50, verbose_name='Station Name', null=False)
    station_symbol = models.CharField(unique=True, max_length=5, verbose_name='Station Symbol')

    def __unicode__(self):  # We need this function bc Django needs a reference to the database table Station
        return unicode(self.station_name) # station_name becomes the reference



# ==== TRAIN ====
#
#   train_num     | start_station | train_ends | train_direction | train_days |
# ----------------|---------------|------------|-----------------|------------|
#   int auto pk   |  station_id   | station_id |     bool(S/N)   | what days this train runs |

class Train(models.Model):
    train_number = models.CharField(null=False, max_length=15, verbose_name='Train Number')
    # 1-1 Field already unique by default
    start_station = models.ForeignKey(Station, related_name='s_start', verbose_name='Start Station')
    end_station = models.ForeignKey(Station, related_name='s_end', verbose_name='End Station')
    train_direction = models.BooleanField(help_text='North = 1, South = 0', verbose_name='Direction')
    train_days = models.CharField(max_length=20, verbose_name='Days train runs', help_text='M-T-W-Th-F-S-Su')

    def __unicode__(self):
        return unicode(self.train_number)


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
    # A related_name argument is added to tell django to generate unique names for them
    seg_north_end = models.ForeignKey(Station, related_name='n_end+', verbose_name='Segment North End')
    seg_south_end = models.ForeignKey(Station, related_name='s_end+', verbose_name='Segment South End')
    seg_fare = models.IntegerField(verbose_name='Fare', null=False)
    seg_distance = models.IntegerField(default=0, verbose_name='Mileage Between Stations', null=False)

    def __unicode__(self):
        return unicode(self.seg_north_end)



# ==== SEATS_FREE ====
#
#  seats_free_id  | sf_segment      | sf_date    |   sf_train_num    |
# ----------------|-----------------|------------|-------------------|
#   int auto pk   | segment_id *pk* |  dateField |    train_id *pk*  |

class SeatsFree(models.Model):
    sf_segment = models.ForeignKey(Segment, related_name='seg+', verbose_name='Segment',
                                   help_text='Shows only north-end station of segment')
    sf_train = models.ForeignKey(Train, related_name='sf_train+', verbose_name='Train in Segment')
    sf_date = models.DateTimeField(verbose_name='Date', help_text='All reservations start June 1st 2017, 6:00am')
    # validator sets the max value for count to 448
    sf_count = models.PositiveIntegerField(validators=[MaxValueValidator(448)], verbose_name='Free Seats in Segment',
                                           help_text='0 <= n <= 448')

    # This allows us to create join together two columns
    class Meta:
        unique_together = (('sf_segment', 'sf_train'),)

    def __unicode__(self):
        return unicode(self.sf_train)



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

class TicketTrip(models.Model):
    trip_start_station = models.ForeignKey(Station, related_name='t_start+', verbose_name='Trip Start Station')
    trip_end_station = models.ForeignKey(Station, related_name='t_end+', verbose_name='Trip End Station')
    #trip_direction = models.BooleanField(default=1, help_text='North = 1, South = 0', verbose_name='Direction')
    trip_train = models.ForeignKey(Train, verbose_name='Train')
    trip_fare = models.IntegerField(default=0, blank=True, null=True, verbose_name='Fare')
    trip_pay_method = models.ForeignKey(PaymentMethod, related_name='t_pay', verbose_name='Choose Payment')
    trip_date = models.DateField(verbose_name='Trip Date', blank=True, null=True)
    trip_segment_start = models.ForeignKey(Segment, related_name='s_start+', verbose_name='Segment Start',
                                           help_text='Shows only north-end station of segment', blank=True, null=True)
    trip_segment_end = models.ForeignKey(Segment, related_name='s_end+', verbose_name='Segment End',
                                         help_text='Shows only north-end station of segment', blank=True, null=True)

    def __unicode__(self):
        return self.trip_start_station % ""

    # def get_field_value(self, field):
    #     if isinstance(field, models.CharField) and field.choices:
    #         return getattr(self, 'get_{}_display'.format(field.name))()
    #     return unicode(getattr(self, field.name))
    #
    # def get_fields(self):
    #     # called by the template
    #     return [(field.verbose_name, self.get_field_value(field)) for field in type(self)._meta.fields]


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
    sa_train = models.ForeignKey(Train, related_name='train+', verbose_name='Which Train?')
    sa_station = models.ForeignKey(Station, null=True, related_name='station+', verbose_name='Station Where Train Stops')
    sa_time_in = models.TimeField(verbose_name='Time-In of Train at Station')
    # blank true determines whether the field is required in Django administrator
    sa_time_out = models.TimeField(verbose_name='Time-out of train at Station', null=True, blank=True)

    def __unicode__(self):
        return unicode(self.sa_train)  # expects an unicode as a return, therefore wrap it as a unicode



# https://data.cusp.nyu.edu/filebrowser/#/user/eames01





