"""
VIEWS

Takes in a web request and returns a response (http request)

This method tell that request to render home that hmtl, and that file will be displayed in on the site
that file will contain our GUI

This is also where we will render (present to user) our forms created in forms.py 

"""

from django.shortcuts import render
from .forms import TicketTripForm, PassengerForm

# Create your views here. Nothing to do here, but read comments and understand

def home(request):

    if request.method == "POST":
        print request.POST
    # Adding Form here: must create an instance of the class
    form = TicketTripForm()

    # Adding some context to home.html. It allows us to use some sort of object and bring that into our template
    context = {
        'form': form,
    }


    # render combines the request, the template and the context created.
    return render(request, 'amtrakmain/home.html', context)

