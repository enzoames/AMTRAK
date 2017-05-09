"""
IMPORTANT!

THIS IS WHERE WE POPULATE OUR DATABASE

"""

from django.core.management.base import BaseCommand
from amtrakmain.models import *
from datetime import date, datetime, time, timedelta

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
        # Computing time in & out values
        starting_date_n1 = datetime(2017, 6, 1, 06, 00)
        starting_date = datetime(2017, 6, 1, 06, 10)
        starting_time = datetime(2017, 6, 1, 06, 10).time()
        time_in_deltas = [12, 16, 23, 30, 20, 35, 25, 12, 6, 18, 86, 23, 28, 24, 53, 21, 14, 12, 17, 39, 39, 19, 5]
        final_time_in_values = [starting_date_n1, starting_date]
        starting_date2 = datetime(2017, 6, 1, 06, 05)
        starting_time2 = datetime(2017, 6, 1, 06, 05).time()
        time_out_deltas = [6, 12, 16, 23, 30, 24, 31, 25, 12, 6, 77, 27, 23, 28, 43, 34, 21, 14, 12, 17, 39, 39, 19]
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

        trains_list = Train.objects.all()
        station_list = Station.objects.all()

        # for train in trains_list:
        #       for station in station_list:
        #           i = 0  # final_time_in_values has 1 more than final_time_out_values
        #           StopsAt(sa_train = train, sa_station = station,
        #                   sa_time_in = final_time_in_values[i], sa_time_out = final_time_out_values[i])
        #
        #
        #
        #
        #
        #

        # Another approach, might be useful for different scenario
        # minutes = lambda s, e: (s + datetime.timedelta(minutes=x) for x in xrange((e - s).seconds / 60 + 1))
        #
        # for m in minutes(today, today + datetime.timedelta(minutes=time_in_deltas[i])):
        #     print m.time

    # =======================================
    # =========== HANDLE FUNCTION ===========
    # =======================================

    def handle(self, *args, **options):
        # self._populate_station() ALREADY POPULATED NO NEED TO RUN AGAIN
        # self._populate_trains() ALREADY POPULATED NO NEED TO RUN AGAIN
        self._populate_stopsat()

    # ========================================
    # =========== HELPER FUNCTIONS ===========
    # ========================================

    def calculate(self, ):
