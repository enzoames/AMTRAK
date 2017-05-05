from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    #url(r'^users/$', views.ajax_user_search, name='demo_user_search'),
]
