"""
URL. Nothing to do here, but read comments and understand

These is the only URL we will need for the amtrakmain app. If amtrakmain were to have different pages
the url for those pages will be added here

"""

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.search, name='search'),
    #url(r'^users/$', views.ajax_user_search, name='demo_user_search'),
]

