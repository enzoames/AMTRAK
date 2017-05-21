from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from .forms import showTablesForm
from amtrakmain.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# ===========================================
# ========== REQUEST CALL FUNCTION ==========
# ===========================================


def displayTables(request):
    context = {}
    form = showTablesForm(request.POST or None)

    if request.method == 'POST':
        print " \n REQUEST POST ", request.POST
        print " \n REQUEST TABLE", request.POST['table']

        if form.is_valid():
            context = whichTable(request.POST)
            #context = calculateTable(request.POST)

            if 'output2' in context.keys():
                print "HERE OUTPUT 2"
                return render(request, 'displaydata/datatables_output2.html', context)
            if 'output3' in context.keys():
                print "HERE OUTPUT 3"
                return render(request, 'displaydata/datatables_output3.html', context)
            else:
                return render(request, 'displaydata/datatables_output.html', context)

    else:
        if request.GET.get('page'):
            print " \n\t there is a page"
            context = calculateSchedule(request.GET)
            return render(request, 'displaydata/datatables_output.html', context)

        elif request.GET.get('ticketpage'):
            print " \n\t there are more tickets"
            context = calculateTicket(request.GET)
            return render(request, 'displaydata/datatables_output3.html', context)

        elif request.GET.get('seatpage'):
            print " \n\t there are more seats objects"
            return render(request, 'displaydata/datatables_output2.html', context)

        else:
            context = {
                'form': form,
            }

            return render(request, 'displaydata/datatables_form.html', context)


def whichTable(request_POST):
    if request_POST['table'] == '1':
        context = calculateSchedule(request_POST)
        return context

    if request_POST['table'] == '2':
        context2 = calculateSeats(request_POST)
        return context2

    if request_POST['table'] == '3':
        context3 = calculateTicket(request_POST)
        return context3


def calculateSchedule(request_POST):
    # POSSIBLE CHOICES
    # [(1, "Train Schedule"), (2, "Seats Free"), (3, "Tickets")]

    print " \n IN CALCULATE SCHEDULE TABLE: ", request_POST

    out_list = StopsAt.objects.all()
    paginator = Paginator(out_list, 25)  # Show 25 contacts per page
    page = request_POST.get('page')
    # query = request.GET.get('page')

    try:
        out = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        out = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        out = paginator.page(paginator.num_pages)

    context = {
        'output': out,
    }
    return context


def calculateSeats(request_POST):
    print " \n IN CALCULATE SEATS TABLE: ", request_POST

    # out_list = SeatsFree.objects.raw('SELECT * FROM amtrakmain_seatsfree WHERE sf_count <= 447')
    out_list = SeatsFree.objects.exclude(sf_count=448)
    paginator = Paginator(out_list, 25)
    page = request_POST.get('seatpage')

    try:
        out = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        out = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        out = paginator.page(paginator.num_pages)

    context = {
        'output2': out,
    }
    return context


def calculateTicket(request_POST):
    print " \n IN CALCULATE TICKET TABLE: ", request_POST

    out_list = TicketTrip.objects.all()
    paginator = Paginator(out_list, 25)
    page = request_POST.get('ticketpage')

    try:
        out = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        out = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        out = paginator.page(paginator.num_pages)

    context = {
        'output3': out,
    }
    return context





    # elif request.GET['table'] == '2':
    #     #seats_free_list = SeatsFree.objects.raw('SELECT * FROM amtrakmain_seatsfree WHERE sf_count >= 447')
    #     print "ok"
    #
    # elif request.GET['table'] == '3':
    #     context = {
    #         'output': TicketTrip.objects.all()
    #     }
    #     return context











