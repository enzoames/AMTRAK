from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from .forms import *
from amtrakmain.models import *

# ===========================================
# ========== REQUEST CALL FUNCTION ==========
# ===========================================


def displayTables(request):
    context = {
        'title': "so far so good"
    }
    return render(request, 'displaydata/datatables_form.html', context)