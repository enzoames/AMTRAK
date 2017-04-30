"""
In admin.py we try to make our backend more robust. When running the server locally and visit the Django admin page to
view our tables we need to make sure the data is clearly displayed. list_display allows us to serve the column names 
of our table. 

"""
# Register your models here. NOTHING TO DO HERE

from django.contrib import admin
from .forms import TicketTripForm, PassengerForm
from .models import Station, Train, Passenger, Segment, PaymentMethod, TicketTrip, StopsAt, SeatsFree


class StationAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'station_symbol']  # column names on admin page (verbose_name)

    class Meta:
        model = Station

admin.site.register(Station, StationAdmin)


class TrainAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'start_station', 'end_station', 'train_direction', 'train_days']

    class Meta:
        model = Train

admin.site.register(Train, TrainAdmin)


class PassengerAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'p_l_name', 'billing_address', 'email']

    class Meta:
        model = PassengerForm

admin.site.register(Passenger, PassengerAdmin)


class SegmentAdmin(admin.ModelAdmin):
    list_display = ['seg_north_end', 'seg_south_end', 'seg_fare', 'seg_distance']

    class Meta:
        model = Segment

admin.site.register(Segment, SegmentAdmin)


class SeatsFreeAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'sf_train', 'sf_date', 'sf_count']

    class Meta:
        model = SeatsFree

admin.site.register(SeatsFree, SeatsFreeAdmin)



admin.site.register(PaymentMethod)



class TicketTripAdmin(admin.ModelAdmin):
    list_display = ['trip_start_station', 'trip_end_station', 'trip_train', 'trip_fare', 'trip_pay_method', 'trip_date',
                    'trip_segment_start', 'trip_segment_end']

    # The model here at admin already assumes a 'form'. For data that the user will be inputting on the GUI -- we will
    # want to use a model form.

    # class Meta:
    #     model = TicketTrip

    form = TicketTripForm  # Here we specify the from that was created in forms.py


admin.site.register(TicketTrip, TicketTripAdmin)


class StopsAtAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'sa_station', 'sa_time_in', 'sa_time_out']

    class Meta:
        model = StopsAt

admin.site.register(StopsAt, StopsAtAdmin)


