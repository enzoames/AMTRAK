from django.shortcuts import render

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
            calculate_trip_info = calculateRemainingParts(request.POST)  # returns 3 things - always

            update_info = updateSeatsFree(calculate_trip_info, request.POST['trip_date'])  # returns 2 or 1 things

            if len(update_info) > 1:
                # create a form instance and populate it with data from the request (user input)
                instanceTripTicket = form.save(commit=False)

                # Updating missing information
                instanceTripTicket.trip_segment_start = calculate_trip_info['TripSegmentStart']
                instanceTripTicket.trip_segment_end = calculate_trip_info['TripSegmentEnd']
                instanceTripTicket.trip_fare = calculate_trip_info['TripFare']
                instanceTripTicket.trip_train = update_info['Train']

                # Updating context to be displayed to user
                context = {
                    'start': str(instanceTripTicket.trip_segment_start),
                    'depart_time': str(request.POST['trip_date']) ,
                    'end': str(instanceTripTicket.trip_segment_end),
                    'arrive_time': str(update_info['ArriveDate']),
                    'train': str(update_info['Train']),
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
        'TripSegmentStart': Trip_Segment_Start,
        'TripSegmentEnd': Trip_Segment_End,
        'TripFare': Total_Fare,
    }

    return context


def updateSeatsFree(trip_info, trip_date):
    context = {}

    start_segment = trip_info['TripSegmentStart']
    end_segment = trip_info['TripSegmentEnd']

    seatsFreeObject = SeatsFree.objects.filter(sf_segment=start_segment, sf_date=trip_date)

    # BASE CASE 1 - If didn't find a row with given time, throw a message
    if len(seatsFreeObject) == 0:
        context['title'] = "There are no available trains at this given time. Please choose different time"
        return context

    starting_point = seatsFreeObject[0]
    cursor_point = starting_point
    trip_train = starting_point.sf_train

    # BASE CASE 2 - No Seats
    if starting_point.sf_count == 0:
        message = "Every Ticket in train" + str(trip_train) + ", at this time" + str(cursor_point.sf_date)
        context['title'] = message
        return context

    # Every other case
    if start_segment.id <= end_segment.id:  # Trip Heading North OR if trip is stays within one segment '<='

        list_of_rows = [starting_point]  # keep this list in mind

        # Check whether there's a free seat along the path of the trip
        while cursor_point.sf_segment.id != end_segment.id:
            temp_segment = Segment.objects.get(seg_south_end=cursor_point.sf_segment.seg_north_end)
            row = SeatsFree.objects.get(sf_segment=temp_segment)

            if row.sf_count == 0:
                context['title'] = "Train Booked from this destination please choose a different time"
                return context
            else:
                # THIS PART IS VERY IMPORTANT
                # As I move through the trip I'm saving each row that corresponds to the trip -- to later decrease count
                list_of_rows.append(row)
                # We only need to append if there is an available seat

            cursor_point = row

        decrement_seat(list_of_rows)  # Call function to decrement seat count from SeatsFree Table

        arrive_time = StopsAt.objects.get(sa_train=starting_point.sf_train, sa_station=end_segment.seg_north_end)

        context = {
            'Train': trip_train,
            'ArriveDate': arrive_time.sa_time_in,
            #'TicketNumber': generateTicketNumber(),
        }

        return context

    else:  # Trip South
        list_of_rows = [starting_point]

        while cursor_point.sf_segment.id != end_segment.id:
            temp_segment = Segment.objects.get(seg_north_end=cursor_point.sf_segment.seg_south_end)
            row = SeatsFree.objects.get(sf_segment=temp_segment)

            if row.sf_count == 0:
                context['title'] = "Train Booked from this destination please choose a different time"
                return context
            else:
                list_of_rows.append(row)

            cursor_point = row

        decrement_seat(list_of_rows)

        arrive_time = StopsAt.objects.get(sa_train=starting_point.sf_train, sa_station=end_segment.seg_south_end)

        context = {
            'Train': trip_train,
            'ArriveDate': arrive_time.sa_time_in,
            #'TicketNumber': generateTicketNumber(),
        }

        return context


def decrement_seat(rows):
    for row in rows:
        row.sf_count -= 1
        row.save()  # Saves to Database

        
# def generateTicketNumber():
#     r = []
#     for x in range(10):
#          r.append(random.randint(0, 10))
#     return r










