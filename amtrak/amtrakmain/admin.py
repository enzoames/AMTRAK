from django.contrib import admin
from models import Station, Train, Passenger, Segment, PaymentMethod, TicketTrip, StopsAt, SeatsFree

# Register your models here. NOTHING TO DO HERE

Models = [Station, Train, Passenger, Segment, PaymentMethod, TicketTrip, StopsAt, SeatsFree]

admin.site.register(Models)
