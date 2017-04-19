from django.contrib import admin
from models import Station, Train, Passenger, Segment, PaymentMethod, TicketTrips, StopsAt

# Register your models here. NOTHING TO DO HERE

Models = [Station, Train, Passenger, Segment, PaymentMethod, TicketTrips, StopsAt]

admin.site.register(Models)
