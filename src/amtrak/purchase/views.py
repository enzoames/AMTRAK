from django.shortcuts import render

from amtrakmain.forms import TicketTripForm
from amtrakmain.models import *
# Create your views here.



def purchase(request):
    form = TicketTripForm(request.POST or None)
    if request.method == 'POST':  # This statement is executed when the user clicks on 'buy ticket' button
        print request.POST

        # COMPUTING MISSING PARTS, TRIP_SEGMENT_START, TRIP_SEGMENT_END, TRIP_FARE, TRIP_TRAIN
        calculated_trip_info = calculateRemainingParts(request.POST)

        if form.is_valid():  # Checks the validity of the from they submitted
            # create a form instance and populate it with data from the request (user input)

            print("\t======form is valid=====")
            instanceTripTicket = form.save(commit=False)
            # Updating missing information
            instanceTripTicket.trip_segment_start = calculated_trip_info['TripSegmentStart']
            instanceTripTicket.trip_segment_end = calculated_trip_info['TripSegmentEnd']
            instanceTripTicket.trip_fare = calculated_trip_info['TripFare']

            # TODO: NEED TO display available train before saving to database

            # saving to database
            instanceTripTicket.save()
            # Updating context to be displayed
            context = {
                'title': 'Thank you for booking a ticket',
            }

            return render(request, 'purchase/success.html', context)

    else:
        # Adding some context to search.html. It allows us to use some sort of object and bring that into our template
        context = {
            'form': form,
        }

        return render(request, 'purchase/purchase_ticket.html', context)


# ===============================
# ========== FUNCTIONS ==========
# ===============================


def calculateRemainingParts(request_POST):
    # We store the station id, but we need the station name...
    userSelectedStartTrip = request_POST['trip_start_station']
    userSelectedEndTrip = request_POST['trip_end_station']

    print ('\n\nUser Start Station: ')
    print(userSelectedStartTrip)
    print type(userSelectedStartTrip)

    print ('\n\nUser End Station: ')
    print(userSelectedEndTrip)
    print type(userSelectedEndTrip)

    # Based on the station id that we obtained above we can grab the 'station_name' from Station table
    UserStartTripStation = Station.objects.get(id=userSelectedStartTrip)
    UserEndTripStation = Station.objects.get(id=userSelectedEndTrip)

    print "\n\n USER START STATION NAME", UserStartTripStation
    print "\n\n USER END STATION NAME", UserEndTripStation

    Total_Fare = 0
    segment_list = Segment.objects.all()  # grabs all the objects (rows) from table Segment
    # print "length of list: ", len(segment_list) == 24

    if UserStartTripStation.id < UserEndTripStation.id:  # Trip Heading North
        # This is the segment where the passenger's trip starts
        Trip_Segment_Start = Segment.objects.get(seg_south_end=UserStartTripStation)
        # This is the segment where the passenger's trip ends
        Trip_Segment_End = Segment.objects.get(seg_north_end=UserEndTripStation)

        print "\n\n TRIP SEGMENT START", Trip_Segment_Start  # has id
        print "\n\n TRIP SEGMENT END", Trip_Segment_End  # has id

        # Now, need to calculate the fare based on the segments calculated above
        for seg in range(len(segment_list)):
            if segment_list[seg].id >= Trip_Segment_Start.id:
                Total_Fare += segment_list[seg].seg_fare
                print "\tFARE: ", Total_Fare
            if segment_list[seg].id == Trip_Segment_End.id:
                break

    else:  # Trip heading south
        Trip_Segment_Start = Segment.objects.get(seg_north_end=UserStartTripStation)
        Trip_Segment_End = Segment.objects.get(seg_south_end=UserEndTripStation)

        print "\n\n TRIP SEGMENT START", Trip_Segment_Start  # has id
        print "\n\n TRIP SEGMENT END", Trip_Segment_End  # has id

        for seg in xrange(len(segment_list), 0, -1):
            if segment_list[seg-1].id <= Trip_Segment_Start.id:
                Total_Fare += segment_list[seg-1].seg_fare
            if segment_list[seg-1].id == Trip_Segment_End:
                break

    remaining_information = {
        'TripSegmentStart': Trip_Segment_Start,
        'TripSegmentEnd': Trip_Segment_End,
        'TripFare': Total_Fare,
        #'Triptrain': None,
    }

    return remaining_information

