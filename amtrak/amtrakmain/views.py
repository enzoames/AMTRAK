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
    print request
    context = {}

    if request.method == 'POST':
        form = TicketTripForm(request.POST or None)
        print request.POST
        # print request.POST['trip_start_station']  # type is unicode
        # print request.POST.get('trip_start_station')
        # print "SMART TEXT:", smart_text(request.POST.get('trip_start_station'), encoding='utf-8')

        # This method is executed when the user clicks on 'buy ticket' button and as long as everything in
        # forms.TicketTripForm is valid and works fine.
        if form.is_valid():
            print ('Form is Valid...')
            # create a form instance and populate it with data from the request (user input)
            # instance = TicketTripForm(request.POST)  # This process is called binding data to the form
            SaveTripTicket = form.save(commit=False)

            userSelectedStartTrip = request.POST['trip_start_station']
            userSelectedEndTrip = request.POST['trip_end_station']



            #def calculateSegements

            #instance_TicketTrip = TicketTrip.objects.raw()

            # SaveTripTicket.trip_segment_start =
            # SaveTripTicket.trip_segment_end =
            # SaveTripTicket.trip_fare =
            # SaveTripTicket.trip_train =

            #model = TicketTrip()

            # Do something here if needed; Calculate other the remaining columns of the database

            form.save()  # Save to Database
            # Updating form to display new context
            context = {
                'title': 'Thank you for booking a ticket',
            }

    else:
        title = 'Welcome'
        # Adding Form here: must create an instance of the class
        form = TicketTripForm(request.POST or None)

        # Adding some context to home.html. It allows us to use some sort of object and bring that into our template
        context = {
            'title': title,
            'form': form,
        }


    # render combines the request, the template and the context created.
    return render(request, 'amtrakmain/home.html', context)
    # Moreover, whenever the user clicks the 'buy ticket' button, it sends a request back to this view. This file works
    # as a constant loop.




