"""
forms.py (default name) is necessary to connect the database to the front end. When the user wants to book a ticket we 
need to create a form for the user to fill out. Then, whenever the form is saved it will be added to the database

Validating data: 

"""

from django import forms
from .models import *
import datetime


# This class will generate a search form if there is an available train and if it has empty seats based on the the
# user input of start_station, end_station, and time.
class SearchTrainForm(forms.Form):
    start = forms.ModelChoiceField(queryset=Station.objects.all())
    end = forms.ModelChoiceField(queryset=Station.objects.all())
    date = forms.DateTimeField(input_formats=['%Y-%m-%d %H:%M:%S'],
                               help_text="Example date: 2017-06-01 06:00:00",
                               widget=forms.DateTimeInput(format='%Y-%m-%d %H:%M:%S'))
    #date = forms.TimeField(widget=forms.MultipleChoiceField(required=True, choices=TIMES,))

    # CREATE VALIDATION FOR DATE !!!!!


class TicketTripForm(forms.ModelForm):

    class Meta:
        model = TicketTrip  # specifying which model we are creating a form for
        # Now, we need to explicitly declare what fields will be included in this form ( Fields to be displayed on the
        # front-end side). The fields are the columns in the model TicketTrips
        fields = ('trip_start_station', 'trip_end_station', 'trip_pay_method', 'trip_date')


class PassengerForm(forms.ModelForm):

    class Meta:
        model = Passenger
        fields = ['p_f_name', 'p_l_name', 'billing_address', 'email']

    def clean_email(self):
        email = self.cleaned_data.get('email')  # Checks for email structure to be valid, ex: 'e.amespizarro@gmail.com'

        emailBase, emailProvider = email.split('@')
        domain, extension = emailProvider.split('.')

        if not extension == 'edu':
            raise forms.ValidationError('Please enter a college email: "example@college.edu" ')

        return email




