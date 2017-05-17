"""
IMPORTANT!

THIS IS WHERE WE POPULATE OUR DATABASE

"""

from django.core.management.base import BaseCommand
from amtrakmain.models import *
from datetime import date, datetime, time, timedelta
from dateutil.relativedelta import relativedelta
import calendar

class Command(BaseCommand):
    args = '<foo bar ...>'
    help = 'our help string comes here'

    # ===============================================
    # =========== POPULATE STATIONS TABLE ===========
    # ===============================================

    def _populate_station(self):
        station_names = [ "Union Station | Washington, DC", "New Carrollton, MD", "BWI Marshall Airport, MD",
                          "Penn Station | Baltimore, MD", "Aberdeen, MD", "J.R.Biden | Wilmington, DE",
                          "30th Street Station | Philadelphia, PA", "Trenton, NJ", "Metropark, NJ",
                          "Newark Liberty Intl. Air., NJ", "Newark, NJ", "Penn Station | New York, NY",
                          "New Rochelle, NY", "Stamford, CT", "Bridgeport, CT", "New Haven, CT", "Old Saybrook, CT",
                          "New London, CT", "Mystic, CT", "Westerly, RI", "Kingston, RI", "Providence, RI",
                          "Route 128, MA", "Back Bay Station | Boston, MA" "South Station | Boston, MA",]

        station_symbols = ["1WDC", "2NCMD", "3MAMD", "4PSBM", "5AMD", "6JRBW", "7SSPP", "8TNJ", "9MNJ", "10NLI",
                           "11NNJ","12PSN", "13NRN", "14SCT", "15BCT", "16NHC", "17OSC", "18NLC", "19MCT", "20WRI",
                           "21KRI", "22PRI", "23RMA", "24BBS", "25SSB"]

        for i in range(len(station_names)):
            instance = Station(station_name=station_names[i], station_symbol=station_symbols[i])
            instance.save()

        print ("\n STATION TABLE POPULATED SUCCESSFULLY\n")

    # =============================================
    # =========== POPULATE TRAINS TABLE ===========
    # =============================================

    def _populate_trains(self):
        train_numbers = ["1North", "2North", "3North", "4North", "5North", "6North", "7North", "8North", "1South",
                         "2South", "3South", "4South", "5South", "6South", "7South", "8South"]

        station_list = Station.objects.all()

        # Loop for North Bound Trains

        for i in range(len(train_numbers)):
            if i <= 7:
                instance = Train(train_number=train_numbers[i], start_station=station_list[0],
                                 end_station=station_list[24], train_direction=1, train_days='M-T-W-Th-F-S-Su')
                instance.save()
            if i > 7:
                instance = Train(train_number=train_numbers[i], start_station=station_list[24],
                                 end_station=station_list[0], train_direction=0, train_days='M-T-W-Th-F-S-Su')
                instance.save()

        print ("\n TRAINS TABLE POPULATED SUCCESSFULLY\n")

    # ===============================================
    # =========== POPULATE STOPS AT TABLE ===========
    # ===============================================

    def _populate_stopsat(self):
        # If train arrives at station A at 6am and leaves at 6:10 -> time delta is 10
        # Same for time_out deltas

        # Time Deltas for North Bound Trains
        north_time_in_deltas = [10, 12, 16, 23, 30, 20, 35, 25, 12, 6, 18, 86, 23, 28, 24, 53, 21, 14, 12, 17, 39, 39, 19, 5]
        north_time_out_deltas = [6, 12, 16, 23, 30, 24, 31, 25, 12, 6, 77, 27, 23, 28, 43, 34, 21, 14, 12, 17, 39, 39, 19, 000]

        # Gets North Bound Trains
        trains_list = Train.objects.filter(train_direction=1)
        station_list = Station.objects.all()

        starting_dates_list = self.generateDates()
        count = 0
        for train in trains_list:
            i = 0
            # call helper function
            final_time = self.calculateTime_IN_OUT(starting_dates_list[count], north_time_in_deltas, north_time_out_deltas)
            for station in station_list:
                instance = StopsAt(sa_train=train, sa_station=station, sa_time_in=final_time[0][i],
                                   sa_time_out=final_time[1][i])
                if final_time[1][i] < final_time[0][i]:  # We reached the last stop of train - no sa_time_out
                    instance = StopsAt(sa_train=train, sa_station=station, sa_time_in=final_time[0][i])

                instance.save()
                i += 1

            count += 1

        # Time Deltas for South Bound Trains
        south_time_in_deltas = [19, 39, 39, 17, 12, 14, 21, 53, 24, 28, 23, 27, 77, 6, 12, 25, 35, 20, 30, 23, 16, 12, 10, 5]
        south_time_out_deltas = [15, 39, 39, 17, 12, 14, 21, 53, 43, 9, 23, 86, 18, 6, 12, 25, 35, 24, 30, 19, 16, 12, 10, 0]

        # Gets South Bound Trains
        trains_list = Train.objects.filter(train_direction=0)
        station_list = Station.objects.all()

        starting_dates_list = self.generateDates()
        count = 0
        for train in trains_list:
            i = 0
            final_time = self.calculateTime_IN_OUT(starting_dates_list[count], south_time_in_deltas, south_time_out_deltas)
            for station in reversed(station_list):  # start iterating from te back
                instance_south = StopsAt(sa_train=train, sa_station=station, sa_time_in=final_time[0][i],
                                         sa_time_out=final_time[1][i])
                if final_time[1][i] < final_time[0][i]:  # We reached the last stop of train - no sa_time_out
                    instance_south = StopsAt(sa_train=train, sa_station=station, sa_time_in=final_time[0][i])

                instance_south.save()
                i += 1

            count += 1

        print ("\n STOPSAT TABLE POPULATED SUCCESSFULLY\n")

    # ===============================================
    # =========== POPULATE SEGMENT TABLE ============
    # ===============================================

    def _populate_segement(self):

        distance = [0, 10, 19, 10, 28, 37, 25, 30, 33, 12, 4, 10, 16, 17, 21, 17, 29, 16, 7, 8, 18, 25, 30, 11, 2, 0]
        fare = [0, 15, 28.5, 15, 42, 55.5, 37.5, 45, 49.5, 18, 6, 15, 24, 25.5, 31.5, 25.5, 43.5, 24, 10.5, 12, 27, 37.5,
                45, 16.5, 3, 0]

        for i in range(1, 25):
            j = i + 1
            retdist = distance[i]
            retfare = fare[i]
            north = Station.objects.get(id=j)
            south = Station.objects.get(id=i)
            instance = Segment(seg_north_end=north, seg_south_end=south, seg_fare=retfare, seg_distance=retdist)
            instance.save()

        print ("\n SEGMENT TABLE POPULATED SUCCESSFULLY\n")

    # =================================================
    # =========== POPULATE SEATSFREE TABLE ============
    # =================================================

    def _populate_seatsfree(self):
        # ===== For Trains going NORTH =====

        train_list = Train.objects.filter(train_direction=1)
        segment_list = Segment.objects.all()

        # Filling up SeatsFree for just the month of June 2017
        year = 2017
        month = 6
        dates = self.generateDatesOfMonth(year, month)  # 2017-06-01 . . . 2017-06-30

        previous_day_out = self.generateDates()
        i = 0

        for train in train_list:
            print "populating train: ", train
            temp_date = previous_day_out[i]

            instance_stack = []  # contains 30 objects at a time

            for segment in segment_list:
                stops_at_instance = StopsAt.objects.get(sa_train=train, sa_station=segment.seg_south_end)
                exact_time = stops_at_instance.sa_time_in

                for d in dates:
                    current_full_date = datetime.combine(d.date(), exact_time)

                    # Check stack for the previous instance
                    for obj in instance_stack:  # find exact object in stack
                        if obj.sf_date.date() == current_full_date.date() and obj.sf_train == stops_at_instance.sa_train:
                            temp_date = obj.sf_date
                            break

                    if temp_date.time() > current_full_date.time():
                        current_full_date = datetime.combine(d.date() + timedelta(days=1), exact_time)

                    instance = SeatsFree(sf_segment=segment, sf_train=train, sf_date=current_full_date, sf_count=448)
                    instance_stack.append(instance)
                    instance.save()

            del instance_stack[:]
            i += 1

        # ===== For Trains going SOUTH =====

        south_train_list = Train.objects.filter(train_direction=0)
        i = 0

        for train in south_train_list:
            print "populating train: ", train
            temp_date = previous_day_out[i]

            instance_stack = []  # contains 30 objects at a time

            for segment in reversed(segment_list):
                stops_at_instance = StopsAt.objects.get(sa_train=train, sa_station=segment.seg_north_end)
                exact_time = stops_at_instance.sa_time_in

                for d in dates:
                    current_full_date = datetime.combine(d.date(), exact_time)

                    # Check stack for the previous instance
                    for obj in instance_stack:  # find exact object in stack
                        if obj.sf_date.date() == current_full_date.date() and obj.sf_train == stops_at_instance.sa_train:
                            temp_date = obj.sf_date
                            break

                    if temp_date.time() > current_full_date.time():
                        current_full_date = datetime.combine(d.date() + timedelta(days=1), exact_time)

                    instance = SeatsFree(sf_segment=segment, sf_train=train, sf_date=current_full_date, sf_count=448)
                    instance_stack.append(instance)
                    instance.save()

            del instance_stack[:]
            i += 1

        print ("\n SEATSFREE TABLE POPULATED SUCCESSFULLY\n")

    # ========================================
    # =========== HELPER FUNCTIONS ===========
    # ========================================

    def generateDatesOfMonth(self, year, month):
        # gets the number of days in the month and year specified
        num_days = calendar.monthrange(year, month)[1]
        # obtain a day object for each day in the month
        days = [datetime(year, month, day) for day in range(1, num_days + 1)]

        return days

    def generateDates(self):
        # Both Directions
        # Morning: 6am | 8am | 10am |||| Afternoon: 12pm | 2pm | 4pm |||| Evening: 6pm | 9pm ||||

        # Starting dates for our trains. For North and South
        date_list = ['2017-06-01 06:00:00', '2017-06-01 08:00:00', '2017-06-01 10:00:00', '2017-06-01 12:00:00',
                     '2017-06-01 14:00:00', '2017-06-01 16:00:00', '2017-06-01 18:00:00', '2017-06-01 21:00:00']

        datetime_object_list = map(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S'), date_list)

        return datetime_object_list

    def calculateTime_IN_OUT(self, starting_date, time_in_deltas, time_out_deltas):
        # starting_date => 2017-06-01 06:00:00
        starting_time = starting_date.time()  # 06:00:00
        final_time_in_values = [starting_date]  # list contains starting date

        # Calculating time_out
        starting_date2 = datetime.combine(starting_date, starting_time) + timedelta(minutes=5)
        starting_time2 = starting_date2.time()  # 06:05:00
        final_time_out_values = [starting_date2]

        for i in range(len(time_in_deltas)):
            temp_time = datetime.combine(starting_date, starting_time) + timedelta(minutes=time_in_deltas[i])
            final_time_in_values.append(temp_time)
            starting_date = temp_time
            starting_time = starting_date.time()

            temp_time2 = datetime.combine(starting_date2, starting_time2) + timedelta(minutes=time_out_deltas[i])
            final_time_out_values.append(temp_time2)
            starting_date2 = temp_time2
            starting_time2 = starting_date2.time()

        final = [final_time_in_values, final_time_out_values]
        return final

    # =======================================
    # =========== HANDLE FUNCTION ===========
    # =======================================

    def handle(self, *args, **options):
        # self._populate_station() ALREADY POPULATED NO NEED TO RUN AGAIN mysql
        # self._populate_trains() ALREADY POPULATED NO NEED TO RUN AGAIN mysql
        # self._populate_stopsat() ALREADY POPULATED NO NEED TO RUN AGAIN mysql
        # self._populate_segement() ALREADY POPULATED NO NEED TO RUN AGAIN mysql
        # self._populate_seatsfree() ALREADY POPULATED NO NEED TO RUN AGAIN mysql
        print "NO NEED TO POPULATE DATABASE"
