from django.shortcuts import render

# Create your views here. Nothing to do here, but read comments and understand

# VIEWS
# Takes in a web request and returns a response (http request)

# This method tell that request to render home that hmtl, and that file will be displayed in on the site
# that file will contain our GUI

def index(request):
    return render(request, 'amtrakmain/home.html')