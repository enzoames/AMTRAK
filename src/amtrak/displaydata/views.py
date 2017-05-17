from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from .forms import showTablesForm
from amtrakmain.models import *

# ===========================================
# ========== REQUEST CALL FUNCTION ==========
# ===========================================


def displayTables(request):
    context = {}

    form = showTablesForm(request.POST or None)

    if request.method == 'POST':
        print request.POST
        print request.POST['table']

        if form.is_valid():

            context = calculateTable(request.POST)

            return render(request, 'displaydata/datatables_output.html', context)

    else:
        context = {
            'form': form,
        }

    return render(request, 'displaydata/datatables_form.html', context)


def calculateTable(request_POST):
    # POSSIBLE CHOICES
    # [(1, "Train Schedule"), (2, "Seats Free"), (3, "Tickets")]

    choice = request_POST['table']

    if int(choice) == 1:
        context = {
            'schedule': StopsAt.objects.all()
            # 'time_in': schedule.sa_time_in,
            # 'station': schedule.sa_station,
            # 'time_out': schedule.sa_time_out,
            # 'train': schedule.sa_train,
        }

        return context

    # elif request_POST['table'] == 2:
    #     seats_free_list = SeatsFree.objects.raw('SELECT * FROM amtrakmain_seatsfree WHERE sf_count >= 447')
    #
    #
    #
    # elif request_POST['table'] == 3:
    #     print "ok"
    #










