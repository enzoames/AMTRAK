from django import forms
from amtrakmain.models import *

class showTablesForm(forms.Form):
    choices_set = [(1, "Train Schedule"), (2, "Seats Free"), (3, "Tickets")]

    table = forms.ChoiceField(choices=choices_set, help_text='Pick one to show data', )
