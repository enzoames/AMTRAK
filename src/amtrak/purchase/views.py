from django.shortcuts import render

# Create your views here.


def purchase(request):
    return render(request, 'purchase/ticket.html', {})
