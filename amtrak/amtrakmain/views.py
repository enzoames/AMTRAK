"""
VIEWS

Takes in a web request and returns a response (http request)

This method tell that request to render home that hmtl, and that file will be displayed in on the site
that file will contain our GUI

This is also where we will render (present to user) our forms created in forms.py 

"""

from django.shortcuts import render
from .forms import TicketTripForm, PassengerForm
from .models import TicketTrip
# from django.utils.encoding import smart_text

# Create your views here. Nothing to do here, but read comments and understand


def home(request):
    # Adding Form here: Either has a "POST' which contains user inputs or None which will be empty form
    form = TicketTripForm(request.POST or None)
    #print form
    print request
    context = {}

    if request.method == 'POST':  # This statement is executed when the user clicks on 'buy ticket' button
        print request.POST
        print request.POST['trip_start_station']  # type is unicode
        # print request.POST.get('trip_start_station')
        # print "SMART TEXT:", smart_text(request.POST.get('trip_start_station'), encoding='utf-8')

        userSelectedStartTrip = request.POST['trip_start_station']

        # blog.object.get()

        userSelectedEndTrip = request.POST['trip_end_station']

        # COMPUTE HERE THE OTHER PARTS OF THE FORM THAT NEED TO BE FILLED OUT

        if form.is_valid():  # Checks the validity of the from they submitted
            print ('Form is Valid...')
            # create a form instance and populate it with data from the request (user input)

            # form.data['segmet'] = computed data

            # instanceTripTicket = form.save(commit=False)



            #instanceTripTicket.trip_segment_start =
            # instanceTripTicket.trip_segment_end =
            # instanceTripTicket.trip_fare =
            # instanceTripTicket.trip_train =






            #instance_TicketTrip = TicketTrip.objects.raw()



            #model = TicketTrip()

            # Do something here if needed; Calculate other the remaining columns of the database

            form.save()  # Save to Database

            # Updating context to be displayed
            context = {
                'title': 'Thank you for booking a ticket',
            }

    else:
        title = 'Welcome'

        # Adding some context to home.html. It allows us to use some sort of object and bring that into our template
        context = {
            'title': title,
            'form': form,
        }

    # render combines the request, the template and the context created.
    return render(request, 'amtrakmain/home.html', context)
    # Moreover, whenever the user clicks the 'buy ticket' button, it sends a request back to this view. This file works
    # as a constant loop.




