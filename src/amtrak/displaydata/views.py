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

            context = calculateTable(request.POST)

            return render(request, 'displaydata/datatables_output.html', context)

    else:
        if request.GET.get('page'):
            print " \n\t there is a page"
            context = calculateTable(request.GET)
            return render(request, 'displaydata/datatables_output.html', context)

        else:
            context = {
                'form': form,
            }

            return render(request, 'displaydata/datatables_form.html', context)


def calculateTable(request_POST):
    # POSSIBLE CHOICES
    # [(1, "Train Schedule"), (2, "Seats Free"), (3, "Tickets")]

    print " \n IN CALCULATE TABLE: ", request_POST

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


    #
    # elif request.GET['table'] == '2':
    #     #seats_free_list = SeatsFree.objects.raw('SELECT * FROM amtrakmain_seatsfree WHERE sf_count >= 447')
    #     print "ok"
    #
    # elif request.GET['table'] == '3':
    #     context = {
    #         'output': TicketTrip.objects.all()
    #     }
    #     return context











