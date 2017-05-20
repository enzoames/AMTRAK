"""
VIEWS

Takes in a web request and returns a response (http request)

This method tell that request to render home that hmtl, and that file will be displayed in on the site
that file will contain our GUI

This is also where we will render (present to user) our forms created in forms.py 

"""

from django.shortcuts import render
from .forms import PassengerForm, SearchTrainForm
from .models import Segment, Station, SeatsFree, StopsAt
from datetime import date, datetime, time, timedelta

# ===========================================
# ========== REQUEST CALL FUNCTION ==========
# ===========================================


def search(request):
    # Dictionary will be used to display information to the user
    context = {}
    # Adding Form here: Either has a "POST' which contains user inputs or None which will be empty form
    form1 = SearchTrainForm(request.POST or None)

    if request.method == 'POST':
        print request.POST

        if form1.is_valid():
            context = searchAvailableTrain(request.POST)

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
    context = {}

    tempChoiceStartStation = Station.objects.get(id=request_POST['start'])  # Specific start station object
    tempChoiceEndStation = Station.objects.get(id=request_POST['end'])  # Specific end station object

    # BASE CASE 1 - Same choice for both
    if tempChoiceStartStation == tempChoiceEndStation:
        context['title'] = "Please choose a different starting or ending station, Thank you"
        return context

    # Every other case
    if tempChoiceStartStation.id < tempChoiceEndStation.id:  # Trip Heading North


        # This is the segment where the passenger's trip starts
        tripSegmentStart = Segment.objects.get(seg_south_end=tempChoiceStartStation)
        tempChoiceDate = request_POST['date']  # Selected date
        # We search in SeatsFree table whether there are any rows that have the given segment and date
        seatsFreeObject = SeatsFree.objects.filter(sf_segment=tripSegmentStart, sf_date=tempChoiceDate)

        # BASE CASE 2 - If didn't find a row with given time, throw a message
        if len(seatsFreeObject) == 0:
            context['title'] = "There are no available trains at this given time. Please choose different time"
            return context

        # startingPoint has attribute segment(has attribute north & south), train, date, and count of open seats
        startingPoint = seatsFreeObject[0]
        cursorPoint = startingPoint

        # BASE CASE 3 - No empty seats
        if startingPoint.sf_count == 0:
            message = "Every Ticket is booked at" + str(tempChoiceStartStation) + "at this time" + str(
                cursorPoint.sf_date)
            context['title'] = message
            return context

        # This is the segment where the passenger's trip ends
        tripSegmentEnd = Segment.objects.get(seg_north_end=tempChoiceEndStation)

        path_train = startingPoint.sf_train  # NEW CODE
        tmp_station = tempChoiceStartStation  # NEW CODE
        trip_date = datetime.strptime(tempChoiceDate, '%Y-%m-%d %H:%M:%S')
        print "TRIP DATE START: ", trip_date
        # Check whether there's a free seat along the path of the trip (Along Free Seats Table)
        while cursorPoint.sf_segment.id != tripSegmentEnd.id:
            tempSegment = Segment.objects.get(seg_south_end=cursorPoint.sf_segment.seg_north_end)
            print "SEGMENTS ALONG THE PATH: ", tempSegment

            tmp_stop = StopsAt.objects.get(sa_train=path_train, sa_station=tempSegment.seg_south_end)  # NEW CODE
            print "STOPSAT INSTANCE to get time_in of that train at that stop:", tmp_stop

            trip_date = datetime.combine(trip_date.date(), tmp_stop.sa_time_in)
            print "SEGMENT:", tempSegment, "LOOK UP TRIP DATE IN SEATSFREE: ", trip_date

            row = SeatsFree.objects.get(sf_segment=tempSegment, sf_date=trip_date)  # NEW CODE


            if row.sf_count == 0:
                context['title'] = "Train Booked from this destination please choose a different time"
                return context

            cursorPoint = row
            tmp_station = cursorPoint.sf_segment.seg_north_end
            trip_date = cursorPoint.sf_date
            print "NEW DATE: ", trip_date

        arrive_time = StopsAt.objects.get(sa_train=startingPoint.sf_train, sa_station=tempChoiceEndStation)

        # Display trip information to user train to user - not saving it!
        context = {
            'title': "Train available - Book before its too late !",
            'start_station': str(tempChoiceStartStation.station_name),
            'depart_date': str(tempChoiceDate),
            'end_station': str(tempChoiceEndStation.station_name),
            'arrive_date': str(arrive_time.sa_time_in),
            'train_number': str(startingPoint.sf_train),
        }

        return context

    else:  # Trip Heading South

        # This is the segment where the passenger's trip starts. NOTE: different from above, we need a different segment
        tripSegmentStart = Segment.objects.get(seg_north_end=tempChoiceStartStation)
        tempChoiceDate = request_POST['date']  # Selected date
        # We search in SeatsFree table whether there are any rows that have the given segment and date
        seatsFreeObject = SeatsFree.objects.filter(sf_segment=tripSegmentStart, sf_date=tempChoiceDate)

        # BASE CASE 2 - If didn't find a row with given time, throw a message
        if len(seatsFreeObject) == 0:
            context['title'] = "There are no available trains at this given time. Please choose different time"
            return context

        # startingPoint has attribute segment(has attribute north & south), train, date, and count of open seats
        startingPoint = seatsFreeObject[0]
        cursorPoint = startingPoint

        # BASE CASE 3 - No empty seats
        if startingPoint.sf_count == 0:
            message = "Every Ticket is booked at" + str(tempChoiceStartStation) + "at this time" + str(
                cursorPoint.sf_date)
            context['title'] = message
            return context

        # This is the segment where the passenger's trip ends
        tripSegmentEnd = Segment.objects.get(seg_south_end=tempChoiceEndStation)

        while cursorPoint.sf_segment.id != tripSegmentEnd.id:
            tempSegment = Segment.objects.get(seg_north_end=cursorPoint.sf_segment.seg_south_end)
            row = SeatsFree.objects.get(sf_segment=tempSegment)

            if row.sf_count == 0:
                context['title'] = "Train Booked from this destination please choose a different time"
                return context

            cursorPoint = row

        arrive_time = StopsAt.objects.get(sa_train=startingPoint.sf_train, sa_station=tempChoiceEndStation)

        context = {
            'title': "Train available - Book before its too late !",
            'start_station': str(tempChoiceStartStation.station_name),
            'depart_date': str(tempChoiceDate),
            'end_station': str(tempChoiceEndStation.station_name),
            'arrive_date': str(arrive_time.sa_time_in),
            'train_number': str(startingPoint.sf_train),
        }

        return context


