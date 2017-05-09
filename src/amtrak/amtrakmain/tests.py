from django.test import TestCase

# Create your tests here. NOTHING TO DO HERE
# Django allows you to create tests, bu we will not be doing any. Not sure how this file works

from datetime import date, datetime, time, timedelta

# time_in = ["06:00:00", "06:10:00", "06:22:00", "06:38:00", "07:01:00", "07:31:00", "07:51:00", "08:26:00",
#            "08:51:00", "09:03:00", "09:09:00", "09:27:00", "10:53:00", "11:16:00", "11:44:00", "12:08:00",
#            "13:01:00", "13:22:00", "13:36:00", "13:48:00", "14:05:00", "14:44:00", "15:23:00", "15:42:00",
#            "15:47:00"]
#
# time_out = ["06:05:00", "06:11:00", "06:23:00", "06:39:00", "07:02:00", "07:32:00", "07:56:00", "08:27:00",
#             "08:52:00", "09:04:00", "09:10:00", "10:27:00", "10:54:00", "11:17:00", "11:45:00", "12:28:00",
#             "13:02:00", "13:23:00", "13:37:00", "13:49:00", "14:06:00", "14:45:00", "15:24:00", "15:43:00"]

starting_date = datetime(2017, 6, 1, 06, 00)
starting_time = datetime(2017, 6, 1, 06, 00).time()
time_in_deltas = [10, 12, 16, 23, 30, 20, 35, 25, 12, 6, 18, 86, 23, 28, 24, 53, 21, 14, 12, 17, 39, 39, 19, 5]
final_time_in_values = [starting_date]
starting_date2 = datetime(2017, 6, 1, 06, 05)
starting_time2 = datetime(2017, 6, 1, 06, 05).time()
time_out_deltas = [6, 12, 16, 23, 30, 24, 31, 25, 12, 6, 77, 27, 23, 28, 43, 34, 21, 14, 12, 17, 39, 39, 19, 000]
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

for t in final_time_in_values:
    print t.time()

print " ====== "

for t in final_time_out_values:
    print t.time()

