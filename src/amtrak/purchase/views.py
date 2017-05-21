from django.shortcuts import render
from datetime import date, datetime, time, timedelta
from amtrakmain.forms import TicketTripForm
from amtrakmain.models import *
# import random

# ============================================
# ========== REQUEST CALL FUNCTIONS ==========
# ============================================


def purchase(request):
    context = {}
    form = TicketTripForm(request.POST or None)
    if request.method == 'POST':  # This statement is executed when the user clicks on 'buy ticket' button
        print request.POST

        if request.POST['trip_start_station'] == request.POST['trip_end_station']:
            context['title'] = "Please choose a different starting or ending station, Thank you"
            return render(request, 'amtrakmain/error.html', context)

        elif form.is_valid():  # Checks the validity of the from before saving
            # COMPUTING MISSING PARTS, TRIP_SEGMENT_START, TRIP_SEGMENT_END, TRIP_FARE
            calculate_trip_info = calculateRemainingParts(request.POST)  # start, end, start_segment, end_segment, fare
            update_info = updateSeatsFree(request.POST)  # title, depart_date, arrive date, train_number

            if len(update_info) > 1:
                # create a form instance and populate it with data from the request (user input)
                instanceTripTicket = form.save(commit=False)

                # Updating missing information
                instanceTripTicket.trip_segment_start = calculate_trip_info['TripSegmentStart']
                instanceTripTicket.trip_segment_end = calculate_trip_info['TripSegmentEnd']
                instanceTripTicket.trip_fare = calculate_trip_info['TripFare']
                instanceTripTicket.trip_train = update_info['train_number']

                # Updating context to be displayed to user
                context = {
                    'title': "Thank you for choosing us. Save your ticket information",
                    'start': str(calculate_trip_info['StartStation']),
                    'depart_time': str(request.POST['trip_date']),
                    'end': str(calculate_trip_info['EndStation']),
                    'arrive_time': str(update_info['arrive_date']),
                    'train': str(update_info['train_number']),
                    'fare': str(instanceTripTicket.trip_fare),
                    #'ticket_number':  ,
                }

                # saving to database
                instanceTripTicket.save()
                # render to front-end
                return render(request, 'purchase/success.html', context)

            else:
                return render(request, 'amtrakmain/error.html', update_info)

    else:
        # Adding some context to search.html. It allows us to use some sort of object and bring that into our template
        context = {
            'form': form,
        }

        return render(request, 'purchase/purchase_ticket.html', context)


# ===========================================
# ========== COMPUTATION FUNCTIONS ==========
# ===========================================


def calculateRemainingParts(request_POST):
    # Grabbing the 'station_name' from Station table based on the user input
    UserStartTripStation = Station.objects.get(id=request_POST['trip_start_station'])
    UserEndTripStation = Station.objects.get(id=request_POST['trip_end_station'])

    Total_Fare = 0
    segment_list = Segment.objects.all()  # grabs all the objects (rows) from table Segment

    if UserStartTripStation.id < UserEndTripStation.id:  # Trip Heading North
        # This is the segment where the passenger's trip starts
        Trip_Segment_Start = Segment.objects.get(seg_south_end=UserStartTripStation)
        # This is the segment where the passenger's trip ends
        Trip_Segment_End = Segment.objects.get(seg_north_end=UserEndTripStation)

        # Now, need to calculate the fare based on the segments calculated above
        for seg in range(len(segment_list)):
            if segment_list[seg].id >= Trip_Segment_Start.id:
                Total_Fare += segment_list[seg].seg_fare
            if segment_list[seg].id == Trip_Segment_End.id:
                break

    else:  # Trip heading south
        Trip_Segment_Start = Segment.objects.get(seg_north_end=UserStartTripStation)
        Trip_Segment_End = Segment.objects.get(seg_south_end=UserEndTripStation)

        for seg in xrange(len(segment_list), 0, -1):
            if segment_list[seg-1].id <= Trip_Segment_Start.id:
                Total_Fare += segment_list[seg-1].seg_fare
            if segment_list[seg-1].id == Trip_Segment_End:
                break

    context = {
        'StartStation': UserStartTripStation,
        'EndStation': UserEndTripStation,
        'TripSegmentStart': Trip_Segment_Start,
        'TripSegmentEnd': Trip_Segment_End,
        'TripFare': Total_Fare,
    }

    return context


def updateSeatsFree(request_POST):
    context = {}

    tempChoiceStartStation = Station.objects.get(id=request_POST['trip_start_station'])  # Specific start station object
    tempChoiceEndStation = Station.objects.get(id=request_POST['trip_end_station'])  # Specific end station object

    # BASE CASE 1 ======= Same choice for both
    if tempChoiceStartStation == tempChoiceEndStation:
        context['title'] = "Please choose a different starting or ending station, Thank you"
        return context

    #  ======= EVERY OTHER CASE =======
    if tempChoiceStartStation.id < tempChoiceEndStation.id:  # Trip Heading North

        # This is the segment where the passenger's trip starts
        tripSegmentStart = Segment.objects.get(seg_south_end=tempChoiceStartStation)
        tempChoiceDate = request_POST['trip_date']  # Selected date
        # We search in SeatsFree table whether there are any rows that have the given segment and date
        seatsFreeObject = SeatsFree.objects.filter(sf_segment=tripSegmentStart, sf_date=tempChoiceDate)

        # ======= BASE CASE A ======= If didn't find a row with given time, throw a message
        if not seatsFreeObject:
            context['title'] = "There are no available trains at this given time. Please choose different time"
            return context

        # startingPoint has attribute segment(has attribute north & south), train, date, and count of open seats
        startingPoint = seatsFreeObject[0]
        cursorPoint = startingPoint

        # ======= BASE CASE B ======= No empty seats
        if startingPoint.sf_count == 0:
            message = "Every Ticket is booked at" + str(tempChoiceStartStation) + "at this time" + str(
                cursorPoint.sf_date)
            context['title'] = message
            return context

        # ======= EVERY OTHER CASE =======
        # This is the segment where the passenger's trip ends
        tripSegmentEnd = Segment.objects.get(seg_north_end=tempChoiceEndStation)

        path_train = startingPoint.sf_train  # NEW CODE
        trip_date = datetime.strptime(tempChoiceDate, '%Y-%m-%d %H:%M:%S')

        all_seats_free = SeatsFree.objects.all()  # get all of the entries so that its cached
        all_stops_at = StopsAt.objects.all()

        list_of_rows = [startingPoint]  # keep this list in mind
        print "TRIP DATE START: ", trip_date
        # Check whether there's a free seat along the path of the trip (Along Free Seats Table)
        while cursorPoint.sf_segment.id != tripSegmentEnd.id:
            tempSegment = Segment.objects.get(seg_south_end=cursorPoint.sf_segment.seg_north_end)
            print "SEGMENTS ALONG THE PATH: ", tempSegment

            tmp_stop = all_stops_at.get(sa_train=path_train, sa_station=tempSegment.seg_south_end)  # NEW CODE
            print "STOPSAT INSTANCE to get time_in of that train at that stop:", tmp_stop

            trip_date = datetime.combine(trip_date.date(), tmp_stop.sa_time_in)
            print "SEGMENT:", tempSegment, "LOOK UP TRIP DATE IN SEATSFREE: ", trip_date

            row = all_seats_free.get(sf_segment=tempSegment, sf_train=path_train, sf_date=trip_date)  # NEW CODE

            if row.sf_count == 0:
                context['title'] = "Train Booked from this destination please choose a different time"
                return context
            else:
                # THIS PART IS VERY IMPORTANT
                # As I move through the trip I'm saving each row that corresponds to the trip -- to later decrease count
                list_of_rows.append(row)
                # We only need to append if there is an available seat

            cursorPoint = row
            # tmp_station = cursorPoint.sf_segment.seg_north_end
            trip_date = cursorPoint.sf_date
            print "NEW DATE: ", trip_date

        arrive_time = StopsAt.objects.get(sa_train=startingPoint.sf_train, sa_station=tempChoiceEndStation)

        # Display trip information to user train to user - not saving it!
        context = {
            'arrive_date': str(arrive_time.sa_time_in),
            'train_number': startingPoint.sf_train,
        }

        decrement_seat(list_of_rows)
        return context

    else:  # Trip Heading South

        # This is the segment where the passenger's trip starts. NOTE: different from above, we need a different segment
        tripSegmentStart = Segment.objects.get(seg_north_end=tempChoiceStartStation)
        tempChoiceDate = request_POST['trip_date']  # Selected date
        # We search in SeatsFree table whether there are any rows that have the given segment and date
        seatsFreeObject = SeatsFree.objects.get(sf_segment=tripSegmentStart, sf_date=tempChoiceDate)

        # ======= BASE CASE A ======= If didn't find a row with given time, throw a message
        if not seatsFreeObject:
            context['title'] = "There are no available trains at this given time. Please choose different time"
            return context

        # startingPoint has attribute segment(has attribute north & south), train, date, and count of open seats
        startingPoint = seatsFreeObject
        cursorPoint = startingPoint

        # ======= BASE CASE B ======= No empty seats
        if startingPoint.sf_count == 0:
            message = "Every Ticket is booked at" + str(tempChoiceStartStation) + "at this time" + str(cursorPoint.sf_date)
            context['title'] = message
            return context

        # ======= EVERY OTHER CASE =======
        # This is the segment where the passenger's trip ends
        tripSegmentEnd = Segment.objects.get(seg_south_end=tempChoiceEndStation)

        path_train = startingPoint.sf_train  # NEW CODE
        trip_date = datetime.strptime(tempChoiceDate, '%Y-%m-%d %H:%M:%S')

        all_seats_free = SeatsFree.objects.all()  # get all of the entries so that its cached
        all_stops_at = StopsAt.objects.all()

        list_of_rows = [startingPoint]  # keep this list in mind

        while cursorPoint.sf_segment.id != tripSegmentEnd.id:
            tempSegment = Segment.objects.get(seg_north_end=cursorPoint.sf_segment.seg_south_end)

            tmp_stop = all_stops_at.get(sa_train=path_train, sa_station=tempSegment.seg_north_end)  # NEW CODE

            trip_date = datetime.combine(trip_date.date(), tmp_stop.sa_time_in)
            print "SEGMENT:", tempSegment, "LOOK UP TRIP DATE IN SEATSFREE: ", trip_date

            row = all_seats_free.get(sf_segment=tempSegment, sf_train=path_train, sf_date=trip_date)  # NEW CODE

            if row.sf_count == 0:
                context['title'] = "Train Booked from this destination please choose a different time"
                return context
            else:
                # THIS PART IS VERY IMPORTANT
                # As I move through the trip I'm saving each row that corresponds to the trip -- to later decrease count
                list_of_rows.append(row)
                # We only need to append if there is an available seat

            cursorPoint = row
            # tmp_station = cursorPoint.sf_segment.seg_north_end
            trip_date = cursorPoint.sf_date
            print "NEW DATE: ", trip_date

        arrive_time = StopsAt.objects.get(sa_train=startingPoint.sf_train, sa_station=tempChoiceEndStation)

        context = {
            'arrive_date': str(arrive_time.sa_time_in),
            'train_number': startingPoint.sf_train,
        }
        decrement_seat(list_of_rows)
        return context


def decrement_seat(rows):
    for row in rows:
        row.sf_count -= 1
        row.save()  # Saves to Database


# def updateSeatsFree(trip_info, trip_date):
#     context = {}
#
#     start_segment = trip_info['TripSegmentStart']
#     end_segment = trip_info['TripSegmentEnd']
#
#     seatsFreeObject = SeatsFree.objects.filter(sf_segment=start_segment, sf_date=trip_date)
#
#     """
#     START HERE: CHECK IF TRAIN IS GOING NORTH OR SOUTH, DO THE SAME AS SEARCH FUNCTION. NEED TO REWRITE EVERYTHING
#     """
#     # ===== BASE CASE 1 ===== - If didn't find a row with given time, throw a message
#     if not seatsFreeObject:
#         context['title'] = "There are no available trains at this given time. Please choose different time"
#         return context
#
#     starting_point = seatsFreeObject[0]
#     cursor_point = starting_point
#     trip_train = starting_point.sf_train
#
#     # ===== BASE CASE 2 ===== No Seats
#     if starting_point.sf_count == 0:
#         message = "Every Ticket in train" + str(trip_train) + ", at this time" + str(cursor_point.sf_date)
#         context['title'] = message
#         return context
#
#     # ===== EVERY OTHER CASE =====
#     if start_segment.id <= end_segment.id:  # Trip Heading North OR if trip is stays within one segment '<='
#
#         list_of_rows = [starting_point]  # keep this list in mind
#
#         # Check whether there's a free seat along the path of the trip
#         while cursor_point.sf_segment.id != end_segment.id:
#             temp_segment = Segment.objects.get(seg_south_end=cursor_point.sf_segment.seg_north_end)
#             row = SeatsFree.objects.get(sf_segment=temp_segment)
#
#             if row.sf_count == 0:
#                 context['title'] = "Train Booked from this destination please choose a different time"
#                 return context
#             else:
#                 # THIS PART IS VERY IMPORTANT
#                 # As I move through the trip I'm saving each row that corresponds to the trip -- to later decrease count
#                 list_of_rows.append(row)
#                 # We only need to append if there is an available seat
#
#             cursor_point = row
#
#         decrement_seat(list_of_rows)  # Call function to decrement seat count from SeatsFree Table
#
#         arrive_time = StopsAt.objects.get(sa_train=starting_point.sf_train, sa_station=end_segment.seg_north_end)
#
#         context = {
#             'Train': trip_train,
#             'ArriveDate': arrive_time.sa_time_in,
#             #'TicketNumber': generateTicketNumber(),
#         }
#
#         return context
#
#     else:  # Trip South
#         list_of_rows = [starting_point]
#
#         while cursor_point.sf_segment.id != end_segment.id:
#             temp_segment = Segment.objects.get(seg_north_end=cursor_point.sf_segment.seg_south_end)
#             row = SeatsFree.objects.get(sf_segment=temp_segment)
#
#             if row.sf_count == 0:
#                 context['title'] = "Train Booked from this destination please choose a different time"
#                 return context
#             else:
#                 list_of_rows.append(row)
#
#             cursor_point = row
#
#         decrement_seat(list_of_rows)
#
#         arrive_time = StopsAt.objects.get(sa_train=starting_point.sf_train, sa_station=end_segment.seg_south_end)
#
#         context = {
#             'Train': trip_train,
#             'ArriveDate': arrive_time.sa_time_in,
#             #'TicketNumber': generateTicketNumber(),
#         }
#
#         return context
        
# def generateTicketNumber():
#     r = []
#     for x in range(10):
#          r.append(random.randint(0, 10))
#     return r










