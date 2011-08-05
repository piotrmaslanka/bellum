from django.conf.urls.defaults import *

urlpatterns = patterns('bellum.chat',

#    (r'^garrison/land/$','garrison.land'),


    (r'^query/', 'ajax.query'),
    (r'^push/', 'ajax.push'),
    (r'^convp/(?P<acc_id>\d+)/$', 'ajax.convp'),
    (r'^convr/$', 'ajax.convr'),
    (r'^retr/(?P<pvmsg_id>\d+)/$', 'ajax.retr'),
    (r'^cache/$', 'ajax.cache'),        # expects GET accid and empire
    (r'^getid/$', 'ajax.obtain_id'),        # expects GET empire
    (r'^relay/(?P<msg_id>\d+)?/(?P<acc_id>\d+)/$', 'ajax.relay'),

)
