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
        # List of staring dates for each train at their starting station
        starting_dates_list = self.generateDates()

        time_in_deltas = [10, 12, 16, 23, 30, 20, 35, 25, 12, 6, 18, 86, 23, 28, 24, 53, 21, 14, 12, 17, 39, 39, 19, 5]
        time_out_deltas = [6, 12, 16, 23, 30, 24, 31, 25, 12, 6, 77, 27, 23, 28, 43, 34, 21, 14, 12, 17, 39, 39, 19,
                           000]

        trains_list = Train.objects.all()
        station_list = Station.objects.all()

        for train in trains_list:
            #call helper function
            self.calculateTime_IN_OUT(starting_date, time_in_deltas, time_out_deltas)
            for station in station_list:
                i = 0  # final_time_in_values has 1 more than final_time_out_values
                StopsAt(sa_train = train, sa_station = station,
                        sa_time_in = final_time_in_values[i], sa_time_out = final_time_out_values[i])


        # Another approach, might be useful for different scenario
        # minutes = lambda s, e: (s + datetime.timedelta(minutes=x) for x in xrange((e - s).seconds / 60 + 1))
        #
        # for m in minutes(today, today + datetime.timedelta(minutes=time_in_deltas[i])):
        #     print m.time

    # ========================================
    # =========== HELPER FUNCTIONS ===========
    # ========================================

    def calculateTime_IN_OUT(self, starting_date, time_in_deltas, time_out_deltas):
        # *Initial value for time_in for any train*
        # starting_date => 2017-06-01 06:00:00
        starting_time = starting_date.time()  # 06:00:00
        final_time_in_values = [starting_date]  # list contains starting date

        # *Initial value for time_out for any train*
        # This gives 2017-06-01 06:05:00
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


    def generateDates(self):
        # Morning: 6am | 8am | 10am |||| Afternoon: 12pm | 2pm | 4pm |||| Evening: 6pm | 8pm ||||
        deltas = []

        date_list = []

        datetime(2017, 6, 1, 06, 00)

        return date_list

    # =======================================
    # =========== HANDLE FUNCTION ===========
    # =======================================

    def handle(self, *args, **options):
        # self._populate_station() ALREADY POPULATED NO NEED TO RUN AGAIN
        # self._populate_trains() ALREADY POPULATED NO NEED TO RUN AGAIN
        self._populate_stopsat()






            # time_in = ["06:00:00", "06:10:00", "06:22:00", "06:38:00", "07:01:00", "07:31:00", "07:51:00", "08:26:00",
        #            "08:51:00", "09:03:00", "09:09:00", "09:27:00", "10:53:00", "11:16:00", "11:44:00", "12:08:00",
        #            "13:01:00", "13:22:00", "13:36:00", "13:48:00", "14:05:00", "14:44:00", "15:23:00", "15:42:00",
        #            "15:47:00"]
        #
        # time_out = ["06:05:00", "06:11:00", "06:23:00", "06:39:00", "07:02:00", "07:32:00", "07:56:00", "08:27:00",
        #             "08:52:00", "09:04:00", "09:10:00", "10:27:00", "10:54:00", "11:17:00", "11:45:00", "12:28:00",
        #             "13:02:00", "13:23:00", "13:37:00", "13:49:00", "14:06:00", "14:45:00", "15:24:00", "15:43:00"]