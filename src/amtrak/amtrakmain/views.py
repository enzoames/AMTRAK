"""
VIEWS

Takes in a web request and returns a response (http request)

This method tell that request to render home that hmtl, and that file will be displayed in on the site
that file will contain our GUI

This is also where we will render (present to user) our forms created in forms.py 

"""

from django.shortcuts import render
from .forms import PassengerForm, SearchTrainForm
from .models import Segment, Station, SeatsFree

# ============================================
# ========== REQUEST CALL FUNCTIONS ==========
# ============================================


def search(request):
    # Dictionary will be used to display information to the user
    context = {}
    # Adding Form here: Either has a "POST' which contains user inputs or None which will be empty form
    form1 = SearchTrainForm(request.POST or None)

    if request.method == 'POST':
        print request.POST

        if form1.is_valid():
            context = searchAvailableTrain(request.POST)

            print context
            # display available trains
            if len(context) > 1:
                return render(request, 'amtrakmain/result.html', context)
            else:
                return render(request, 'amtrakmain/error.html', context)
    else:
        context = {
            'form1': form1,
        }
    # render combines the request, the template and the context created.
    return render(request, 'amtrakmain/search.html', context)
    # Moreover, whenever the user clicks the 'buy ticket' button, it sends a request back to this view. This file works
    # as a constant loop.


# ===========================================
# ========== COMPUTATION FUNCTIONS ==========
# ===========================================


def searchAvailableTrain(request_POST):
    context = {
        'title': ""
    }

    tempChoiceStartStation = request_POST['start']  # grabs user's selected choice for start station, which is an id #
    tempChoiceEndStation = request_POST['end']  # grabs user's selected choice for end station, which is an id #

    tempChoiceStartStation = Station.objects.get(id=tempChoiceStartStation)  # Specific start station
    tempChoiceEndStation = Station.objects.get(id=tempChoiceEndStation)  # Specific end station

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
            # cursorPoint has attribute segment(has attribute north & south), train, date, and count of open seats
            startingPoint = seatsFreeObjects[0]
            cursorPoint = startingPoint

            if cursorPoint.sf_count == 0:
                message = "Every Ticket is booked at" + str(tempChoiceStartStation) + "at this time" + str(cursorPoint.sf_date)
                context['title'] = message
                return context

            else:
                # This is the segment where the passenger's trip ends
                tripSegmentEnd = Segment.objects.get(seg_north_end=tempChoiceEndStation)

                # Check whether there's a free seat along the path of the trip
                while cursorPoint.sf_segment.id != tripSegmentEnd.id:

                    tempSegment = Segment.objects.get(seg_south_end=cursorPoint.sf_segment.seg_north_end)
                    row = SeatsFree.objects.get(sf_segment=tempSegment)

                    if row.sf_count == 0:
                        context['title'] = "Train Booked from destination A to B, please choose a different time"
                        return context

                    cursorPoint = row

                # Display trip information to user train to user - not saving it!
                context = {
                    'title': "Train available",
                    'start_station': str(tempChoiceStartStation.station_name),
                    'depart_time': str(tempChoiceDate),
                    'end_station': str(tempChoiceEndStation.station_name),
                    # 'arrival_time':
                    'train_number': str(startingPoint.sf_train),
                    # 'trip_date':
                }

                return context

    else: # Trip heading south
        Trip_Segment_Start = Segment.objects.get(seg_north_end=tempChoiceStartStation)
        Trip_Segment_End = Segment.objects.get(seg_south_end=tempChoiceEndStation)


    context['title'] = "NO TITLE"
    return context






# def home(request):
#     return render('search.html', {}, context_instance=RequestContext(request))
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
#     return render(request, 'amtrakmain/search.html', context)





