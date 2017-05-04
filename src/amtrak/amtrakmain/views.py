"""
VIEWS

Takes in a web request and returns a response (http request)

This method tell that request to render home that hmtl, and that file will be displayed in on the site
that file will contain our GUI

This is also where we will render (present to user) our forms created in forms.py 

"""

from django.shortcuts import render
from .forms import TicketTripForm, PassengerForm, SearchTrainForm
from .models import TicketTrip, Segment, Station, Train, SeatsFree
# from django.utils.encoding import smart_text

from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.db.models import Q
#from django.contrib.auth.models import User
import time


# ============================================
# ========== REQUEST CALL FUNCTIONS ==========
# ============================================


def search(request):
    context = {}
    form1 = SearchTrainForm(request.POST or None)

    if request.method == 'POST':
        print request.POST

        if form1.is_valid():
            context = searchAvailableTrain(request.POST)

            print context
            # display available trains

            return render(request, 'amtrakmain/result.html', context)

    else:
        context = {
            'form1': form1,
        }

    return render(request, 'amtrakmain/home.html', context)


# ===========================================
# ========== COMPUTATION FUNCTIONS ==========
# ===========================================


def searchAvailableTrain(request_POST):
    # Dictionary will be used to display information
    context = {
        'title': ""
    }

    tempChoiceStartStation = request_POST['start'] # grabs user's selected choice for start station
    tempChoiceEndStation = request_POST['end'] # grabs user's selected choice for end station

    tempChoiceStartStation = Station.objects.get(id=tempChoiceStartStation)
    tempChoiceEndStation = Station.objects.get(id=tempChoiceEndStation)

    # Base Case
    if tempChoiceStartStation == tempChoiceEndStation:
        context['title'] = "Please choose a different start station or end station, Thank you"
        return context

    # Every other case
    if tempChoiceStartStation.id < tempChoiceEndStation.id:  # Trip Heading North
        # This is the segment where the passenger's trip starts
        tripSegmentStart = Segment.objects.get(seg_south_end=tempChoiceStartStation)

        tempChoiceDate = request_POST['date']
        # We search in SeatsFree table whether there are any rows that have the given segment and date
        seatsFreeObjects = SeatsFree.objects.filter(sf_segment=tripSegmentStart, sf_date=tempChoiceDate)

        # If didn't find a row with given time, throw a message
        if len(seatsFreeObjects) == 0:
            context['title'] = "There are no available trains at this given time"
            return context

        # Else continue to look for empty seats in trip
        else:
            # seatsFreeObjects should be narrow down to one single train, unique time, and one single start station
            print "FIND SEATS"
            print type(seatsFreeObjects)
            print len(seatsFreeObjects)
            print seatsFreeObjects
            print seatsFreeObjects[0]

            # startingPoint has attribute segment(has attribute north & south), train, date, and count of open seats
            startingPoint = seatsFreeObjects[0]

            if startingPoint.sf_count == 0:
                message = "Every Ticket is booked at" + str(tempChoiceStartStation) + "at this time" + str(startingPoint.sf_date)
                context['title'] = message
                return context

            else:
                print "++++++++++++++++++++======================="
                print "FIRST SEGMENT IN LINE"
                print "north ", startingPoint.sf_segment.seg_north_end, "\tsouth: ", startingPoint.sf_segment.seg_south_end

                """
                while True:
                    tempSegment = Segment.objects.get(seg_south_end=startingPoint.sf_segment.seg_north_end)

                    row = SeatsFree.objects.get(sf_segment=tempSegment)

                    if row.sf_count == 0:
                        context['title'] = "Train Booked from destination A to B, please choose a different time"
                        return context
                """

                # TODO: MODIFY WHILE TRUE STATEMENT. TRAVERSE THROUGH THE SEGMENTS TABLE AND SEATS FREE TABLE
                # TODO: STARTING POINT =  STARTING POINT. NEXT

                # print "NEXT SEGMENT ON LINE"
                # print "segment north", row.sf_segment.seg_north_end, "\ttrain", row.sf_train, "\ndate", row.sf_date
                # print "segment south", row.sf_segment.seg_south_end



        # This is the segment where the passenger's trip ends
        # tripSegmentEnd = Segment.objects.get(seg_north_end=tempChoiceEndStation)


    else: # Trip heading south
        Trip_Segment_Start = Segment.objects.get(seg_north_end=tempChoiceStartStation)
        Trip_Segment_End = Segment.objects.get(seg_south_end=tempChoiceEndStation)

    context['title'] = "NO TITLE"
    return context


    #tempStartSegment = Segment.objects.get(id=tempChoiceStartStation) # from segments table

    # print seatsFreeObject.sf_segment, seatsFreeObject.sf_train, seatsFreeObject.sf_date, seatsFreeObject.sf_count
    #
    # if seatsFreeObject.sf_count > 1:











# def home(request):
#     return render('home.html', {}, context_instance=RequestContext(request))
#
# def ajax_user_search(request):
#
#     if request.is_ajax():
#         q = request.GET.get( 'q' )
#         if q is not None:
#             results = User.objects.filter(
#                 Q( first_name__contains = q ) |
#                 Q( last_name__contains = q ) |
#                 Q( username__contains = q ) ).order_by( 'username' )
#
#             return render_to_response( 'results.html', { 'results': results, },
#                                        context_instance = RequestContext( request ) )


# def searchTrain(request):
#     train_instance = Train.objects.all()
#     context = {
#         'available_trains': train_instance
#     }
#     return render(request, 'amtrakmain/home.html', context)


# def home(request):
#     # Adding Form here: Either has a "POST' which contains user inputs or None which will be empty form
#     form = TicketTripForm(request.POST or None)
#     context = {}
#     if request.method == 'POST':  # This statement is executed when the user clicks on 'buy ticket' button
#         print request.POST
#
#         # COMPUTING MISSING PARTS, TRIP_SEGMENT_START, TRIP_SEGMENT_END, TRIP_FARE, TRIP_TRAIN
#         calculated_trip_info = calculateRemainingParts(request.POST)
#
#         if form.is_valid():  # Checks the validity of the from they submitted
#             # create a form instance and populate it with data from the request (user input)
#             instanceTripTicket = form.save(commit=False)
#             # Updating missing information
#             instanceTripTicket.trip_segment_start = calculated_trip_info['TripSegmentStart']
#             instanceTripTicket.trip_segment_end = calculated_trip_info['TripSegmentEnd']
#             instanceTripTicket.trip_fare = calculated_trip_info['TripFare']
#
#             # TODO: NEED TO display available train before saving to database
#
#             # saving to database
#             instanceTripTicket.save()
#             # Updating context to be displayed
#             context = {
#                 'title': 'Thank you for booking a ticket',
#             }
#     else:
#         title = 'Welcome'
#         # Adding some context to home.html. It allows us to use some sort of object and bring that into our template
#         context = {
#             'title': title,
#             'form': form,
#         }
#
#     # render combines the request, the template and the context created.
#     return render(request, 'amtrakmain/ticket.html', context)
#     # Moreover, whenever the user clicks the 'buy ticket' button, it sends a request back to this view. This file works
#     # as a constant loop.



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




