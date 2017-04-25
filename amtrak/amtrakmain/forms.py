"""
forms.py (default name) is necessary to connect the database to the front end. When the user wants to book a ticket we 
need to create a form for the user to fill out. Then, whenever the form is saved it will be added to the database

Validating data: 

"""

from django import forms
from .models import Station, Train, Passenger, Segment, PaymentMethod, TicketTrip, StopsAt, SeatsFree


class TicketTripForm(forms.ModelForm):

    class Meta:
        model = TicketTrip  # specifying which model we are creating a form for
        # Now, we need to explicitly declare what fields will be included in this form ( Fields to be displayed on the
        # front-end side). The fields are the columns in the model TicketTrips
        fields = ['trip_start_station', 'trip_end_station', 'trip_pay_method', 'trip_date', 'trip_train', 'trip_fare',
                  'trip_segment_start', 'trip_segment_end']

        # widgets = {'trip_date': forms.DateField(attrs={'class': 'datepicker', 'id': 'data_input', }), }



    # def clean_trip_start_station(self):
    #     t_start = self.cleaned_data.get('trip_start')
    #     # write validation code here
    #     return t_start
    #
    # def clean_trip_end_station(self):
    #     t_end = self.cleaned_data.get('trip_end')
    #     # write validation code here
    #     return t_end
    #
    # def clean_trip_date(self):
    #     t_date = self.cleaned_data.get('trip_date')
    #     # write validation code here
    #     return t_date


    # def clean_trip_segment_start(self):
    #     t_s_start = self.cleaned_data('trip_segment_start')
    #
    #    return t_s_start

    # def clean_trip_segment_end(self):
    #
    # def clean_trip_fare(self):
    #
    # def clean_trip_train(self):


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




